#include <magic.h>
#include <iostream>
#include <sstream>
#include <map>
#include <string>
#include <vector>
#include <sys/stat.h>
#include <cassert>
#include <cstdlib>

#ifndef CONFIG
  #error Must define CONFIG
#endif

#if CONFIG == 1
  #include "config.h"
#elif CONFIG == 2
  #include "osx_config.h"
#else
  #error CONFIG must be 1 or 2
#endif

using namespace std;

string get_file_extension(const string &in_filename) {
  size_t ext_location = in_filename.find_last_of('.');
  if (ext_location != string::npos) {
    return in_filename.substr(ext_location+1);
  } 
  else {
    return "";
  }
}

bool contained_in(const char c, const string& str) {
  for (string::const_iterator iter = str.cbegin(); iter != str.cend(); iter++) {
    if (*iter == c) {
      return true;
    }
  }

  return false;
}

string escape_chars(const string& input, const string &char_set) {
  stringstream stream;

  for (string::const_iterator iter = input.cbegin(); iter != input.cend(); iter++) {
    if (contained_in(*iter, char_set)) {
      stream << "\\";
      stream << *iter;
    }
    else
      stream << *iter;
  }

  return stream.str();
}

int main(int argc, char** argv) {
  if ( argc<2 ) {
    cout << "Please enter a filename." << endl;
    return 1;
  }

  assert(string("foo\\ bar\\(") == escape_chars("foo bar(", " ()"));

  map<string, string> ext_app;
  setup_ext_apps(ext_app);

  map<string, string> mime_app;
  setup_mime_apps(mime_app);

  magic_t magic_cookie = 
    magic_open(MAGIC_MIME_TYPE|MAGIC_SYMLINK);
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

  typedef map<string, vector<string> > mime_files_t;
  mime_files_t mime_files;
  for (int i=1; i<argc; i++) {
    string cur_file = *(argv+i);

    struct stat st_file_info;
    int ret_stat = -1;
    ret_stat = stat(cur_file.c_str(), &st_file_info);

    string cur_app = "";
    if (ret_stat != 0) {
      cout << cur_file << " not found. Creating text file." << endl;
      cur_app = mime_app["text/plain"];

    } else {
      string cur_ext = get_file_extension(cur_file);
      const char* cur_mime_char = magic_file(magic_cookie, cur_file.c_str());
      if (cur_mime_char == NULL) {
        cout << "magic_file failed to retrieve description of contents." << endl;
        cout << "error: " << magic_error(magic_cookie) << endl;
        return 1;
      }
      string cur_mime = string(cur_mime_char);

      // preference is mime then extension
      if (mime_app.find(cur_mime) != mime_app.end()) {
        cur_app = mime_app[cur_mime];
      }
      else if (ext_app.find(cur_ext) != ext_app.end()) {
        cur_app = ext_app[cur_ext];
      }
      else {
        cout << "No app defined for " << cur_mime << " or " << cur_ext << endl;
        continue;
      }
    }

    cur_file = escape_chars(cur_file, " ()[]&");
    mime_files[cur_app].push_back(cur_file);
  }

  for (mime_files_t::const_iterator cmd_iter = mime_files.begin();
       cmd_iter != mime_files.end(); cmd_iter++) {
    string cmd_out;
    cmd_out = cmd_out + cmd_iter->first + " ";

    vector<string> files = cmd_iter->second;
    for (vector<string>::const_iterator file_iter = files.begin();
         file_iter != files.end(); file_iter++) {
      cmd_out = cmd_out + *file_iter + " ";
    }

    cout << cmd_out << endl;
    system(cmd_out.c_str());
  }

  magic_close(magic_cookie);
  return 0;
}
