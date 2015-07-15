#include <magic.h>
#include <iostream>
#include <map>
#include <string>
#include <algorithm>
#include <vector>
#include <cstdlib>
#include <cstdio>
#include <sys/stat.h>
#include <boost/algorithm/string/replace.hpp>

using namespace std;

// return extension of filename
string get_file_ext(const string &in_filename) {
  size_t ext_location = in_filename.find_last_of('.');
  if (  ext_location != string::npos ) {
    return in_filename.substr(ext_location+1);
  } 
  else {
    return "";
  }
}

int main(int argc, char** argv)
{
  if ( argc<2 ) {
    cout << "Please enter a filename." << endl;
    return 1;
  }

  map<string, string> ext_app;
  ext_app["xoj"] = "xournal";
  ext_app["scala"] = "vim -p";

  map<string, string> mime_app;
  mime_app["application/msword"] = "abiword";
  mime_app["application/pdf"] = "zathura";
  mime_app["application/rtf"] = "abiword";
  mime_app["application/vnd.ms-excel"] = "gnumeric";
  mime_app["application/x-perl"] = "vim -p";
  mime_app["application/x-shellscript"] = "vim -p";
  mime_app["application/x-tar"] = "tar -xf";
  mime_app["application/x-xoj"] = "xournal";
  mime_app["application/vnd.ms-office"] = "gnumeric";
  mime_app["image/jpeg"] = "gqview";
  mime_app["text/plain"] = "vim -p";
  mime_app["text/x-c"] = "vim -p";
  mime_app["text/x-c++src"] = "vim -p";
  mime_app["text/x-c++"] = "vim -p";
  mime_app["text/x-csrc"] = "vim -p";
  mime_app["text/x-fortran"] = "vim -p";
  mime_app["text/x-java"] = "vim -p";
  mime_app["text/x-log"] = "vim -p";
  mime_app["text/x-matlab"] = "vim -p";
  mime_app["text/x-pascal"] = "vim -p";
  mime_app["text/x-python"] = "vim -p";
  mime_app["text/x-shellscript"] = "vim -p";
  mime_app["text/x-tex"] = "vim -p";
  mime_app["video/x-ms-wmv"] = "mplayer";
  mime_app["video/x-msvideo"] = "mplayer";

  // load magic
  magic_t magic_cookie = 
    magic_open(MAGIC_MIME_TYPE|MAGIC_SYMLINK|MAGIC_COMPRESS);
  if ( magic_cookie == NULL) {
    cout << "Unable to initialize magic." << endl;
    return 1;
  }
  if ( magic_load(magic_cookie, NULL) != 0 ) {
    cout << "Unable to load magic" <<
      magic_error(magic_cookie) << endl;
    magic_close(magic_cookie);
    return 1;
  }

  // create app/file associations
  typedef map<string, vector<string> > mime_files_t;
  mime_files_t mime_files;
  for (int i=1; i<argc; i++) {
    string cur_file = *(argv+i);
    
    // create blank file if file does not exist.
    struct stat st_file_info;
    int ret_stat = -1;
    ret_stat = stat(cur_file.c_str(), &st_file_info);
    if ( ret_stat != 0 ) {
      cout << cur_file << " not found. Creating text file." << endl;
      mime_files[mime_app["text/plain"]].push_back(cur_file);
      continue;
    } 

    string cur_app = "";

    string cur_ext = get_file_ext(cur_file);
    string cur_mime = magic_file(magic_cookie, cur_file.c_str());

    // preference is mime then extension
    // if app defined for mime_type
    if ( mime_app.find(cur_mime) != mime_app.end() ) {
      cur_app = mime_app[cur_mime];
    }
    // if no mime, if app defined for ext
    else if ( ext_app.find(cur_ext) != ext_app.end() ) {
      cur_app = ext_app[cur_ext];
    }
    // if no mime, no ext
    else {
      cout << "No app defined for " << cur_mime << " or " << cur_ext << endl;
      continue;
    }

    // file exists and mime type program exists
    boost::algorithm::replace_all(cur_file, " ", "\\ ");
    boost::algorithm::replace_all(cur_file, "(", "\\(");
    boost::algorithm::replace_all(cur_file, ")", "\\)");
    boost::algorithm::replace_all(cur_file, "[", "\\[");
    boost::algorithm::replace_all(cur_file, "]", "\\]");
    boost::algorithm::replace_all(cur_file, "&", "\\&");
    mime_files[cur_app].push_back(cur_file);
  }
  
  // build cmd strings
  for ( mime_files_t::const_iterator iter = mime_files.begin(); 
      iter != mime_files.end(); iter++ ) {
    string cmd_out;
    cmd_out = cmd_out + iter->first + " ";
    for ( vector<string>::const_iterator iter2 = (iter->second).begin();
        iter2 != (iter->second).end(); iter2++ ) {
      cmd_out = cmd_out + *iter2 + " ";
    }
    cout << cmd_out << endl;
    system(cmd_out.c_str());
  }

  magic_close(magic_cookie);
  return 0;

}
