#pragma once

void setup_ext_apps(std::map<std::string, std::string>& ext_app) {
  ext_app["xoj"] = "xournal";
  ext_app["scala"] = "vim";
}

void setup_mime_apps(std::map<std::string, std::string>& mime_app) {
  mime_app["application/pdf"] = "zathura";
  mime_app["application/vnd.ms-excel"] = "gnumeric";
  mime_app["application/x-perl"] = "vim";
  mime_app["application/x-shellscript"] = "vim";
  mime_app["application/x-tar"] = "tar -xf";
  mime_app["application/x-xoj"] = "xournal";
  mime_app["application/vnd.ms-office"] = "gnumeric";
  mime_app["image/jpeg"] = "imv";
  mime_app["text/plain"] = "vim";
  mime_app["text/x-c"] = "vim";
  mime_app["text/x-c++src"] = "vim";
  mime_app["text/x-c++"] = "vim";
  mime_app["text/x-csrc"] = "vim";
  mime_app["text/x-fortran"] = "vim";
  mime_app["text/x-java"] = "vim";
  mime_app["text/x-log"] = "vim";
  mime_app["text/x-matlab"] = "vim";
  mime_app["text/x-pascal"] = "vim";
  mime_app["text/x-python"] = "vim";
  mime_app["text/x-shellscript"] = "vim";
  mime_app["text/x-tex"] = "vim";
  mime_app["video/x-ms-wmv"] = "mplayer";
  mime_app["video/x-msvideo"] = "mplayer";
}

