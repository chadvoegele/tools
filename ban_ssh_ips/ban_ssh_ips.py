import sys
import importlib.util
import systemd.journal
import re

def ipRegex():
    ipRegex = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    return ipRegex

def getFiltersCounts():
    filtersCounts = [
            ("%s port \d+:\d: com\.jcraft\.jsch\.JSchException: Auth fail" % ipRegex(), 1),
            ("Invalid user.*%s" % ipRegex(), 2),
            ("Did not receive identification string from %s" % ipRegex(), 1),
            ("fatal: Unable to negotiate with %s port \d+: no matching key exchange method found." % ipRegex(), 1),
            (".*%s.*" % ipRegex(), 25)
            ]
    return filtersCounts

def matchLine(regex, line):
    match = re.search(regex, line) is not None
    return match

def errorIfModuleMissing(name):
    isMissing = importlib.util.find_spec(name) is None
    if isMissing:
        print("Please install module: %s" % name)
        sys.exit(1)

def readJournal(service):
    j = systemd.journal.Reader()
    j.this_boot()
    j.add_match(_SYSTEMD_UNIT=service)
    messages = [entry['MESSAGE'] for entry in j]
    return messages

def getIPFromLine(line):
    match = re.search("(%s)" % ipRegex(), line)
    ip = match.group(0)
    return ip

def getIPsFromLog(lines, regex, atLeastCount):
    filteredLines = [l for l in lines if matchLine(regex, l)]
    ips = [getIPFromLine(l) for l in filteredLines]
    countIPs = [(ip, ips.count(ip)) for ip in set(ips)]
    frequentIPs = [ip for (ip, count) in countIPs if count >= atLeastCount]
    return frequentIPs

def getAllIPs(lines, filtersCounts):
    ips_list = [getIPsFromLog(lines, regex, atLeastCount) for (regex, atLeastCount) in filtersCounts]
    ips = [ip for ips in ips_list for ip in ips]
    ips = set(ips)
    return ips

def iptablesBlockIP(ip):
    iptablesBlock = "-A INPUT -s %s/32 -j DROP" % ip
    return iptablesBlock

def main():
    errorIfModuleMissing('systemd')
    messages = readJournal("sshd.service")
    filtersCounts = getFiltersCounts()
    ips = getAllIPs(messages, filtersCounts)
    print("\n".join([iptablesBlockIP(ip) for ip in ips]))

if __name__ == "__main__":
    main()
