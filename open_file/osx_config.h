#pragma once

void setup_ext_apps(std::map<std::string, std::string>& ext_app) {
  ext_app["scala"] = "vim";
}

void setup_mime_apps(std::map<std::string, std::string>& mime_app) {
  mime_app["application/pdf"] = "open -a /Applications/Preview.app";
  mime_app["application/x-perl"] = "vim";
  mime_app["application/x-shellscript"] = "vim";
  mime_app["application/x-tar"] = "tar -xf";
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
}

