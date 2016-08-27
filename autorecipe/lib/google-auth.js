'use strict';

var google = require('googleapis');
var script = google.script('v1');
var OAuth2Client = google.auth.OAuth2;
var readline = require('readline');

var exports = {};

exports.authenticate = function (args) {
  var oauth2Client = new OAuth2Client(args.clientID, args.clientSecret, args.redirectURL);

  var url = oauth2Client.generateAuthUrl({
    access_type: 'offline', // will return a refresh token
    scope: args.scopes
  });

  var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  console.log('Visit the url: ', url);
  rl.question('Enter the code here: ', function (code) {
    oauth2Client.getToken(code, function (err, tokens) {
      if (err) {
        return args.errCallback(err);
      }
      oauth2Client.setCredentials(tokens);
      args.callback(oauth2Client);
    });
  });
}

exports.runScriptFunction = function (args) {
  return function withArgs () {
    var request = {
      'function': args.functionName,
      'parameters': Array.prototype.slice.call(arguments),
      'devMode': true   // Optional.
    };

    script.scripts.run({
      auth: args.oauth2Client,
      scriptId: args.scriptID,
      resource: request
    }, {}, args.callback);
  };
};

module.exports = exports;
