#pragma once

void setup_ext_apps(std::map<std::string, std::string>& ext_app) {
  ext_app["xoj"] = "xournalpp";
  ext_app["scala"] = "vim -p";
}

void setup_mime_apps(std::map<std::string, std::string>& mime_app) {
  mime_app["application/msword"] = "abiword";
  mime_app["application/pdf"] = "zathura";
  mime_app["application/rtf"] = "abiword";
  mime_app["application/vnd.ms-excel"] = "gnumeric";
  mime_app["application/x-perl"] = "vim -p";
  mime_app["application/x-shellscript"] = "vim -p";
  mime_app["application/x-tar"] = "tar -xf";
  mime_app["application/x-xoj"] = "xournalpp";
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
}

