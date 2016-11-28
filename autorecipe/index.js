#!/usr/bin/env node
'use strict';

var fs = require('fs');
var parseRecipe = require('./lib/parser.js');
var googleAuth = require('./lib/google-auth.js');

// Set as environment variables:
//   CLIENT_ID
//   CLIENT_SECRET
//   REDIRECT_URL
//   SCRIPT_ID
//
// For CLIENT_ID, CLIENT_SECRET,
//   Use https://console.developers.google.com/apis/credentials.
//   For project,
//     Make sure Google Apps Script Execution API is enabled.
//   For Credentials -> OAuth 2.0 client ID,
//     Make sure REDIRECT_URL is in Authorized redirect URIs
// Get SCRIPT_ID from (script.google.com) -> File -> Project Properties -> Project key

function getRecipeFilenames () {
  var filenames;
  if (process.argv[0].search('node') >= 0) {
    filenames = process.argv.slice(2);
  } else {
    filenames = process.argv.slice(1);
  }
  return filenames;
}

function parseRecipes (filenames) {
  var recipes = filenames.map(function (filename) {
    var recipeLines = fs.readFileSync(filename, 'utf8').split('\n');
    var recipe =  parseRecipe(recipeLines);
    return recipe;
  });
  return recipes;
}

var filenames = getRecipeFilenames();
var recipes = parseRecipes(filenames);
googleAuth.authenticate({
  clientID: process.env.CLIENT_ID,
  clientSecret: process.env.CLIENT_SECRET,
  redirectURL: process.env.REDIRECT_URL,
  scopes: [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/script.external_request'
  ],
  errCallback: function () { console.log(JSON.stringify(arguments)); },
  callback: function (oauth2Client) {
    googleAuth.runScriptFunction({
      scriptID: process.env.SCRIPT_ID,
      functionName: 'makeRecipes',
      callback: function () { console.log(JSON.stringify(arguments)); },
      oauth2Client: oauth2Client
    })(recipes, process.env.MOVE_TO);
  }
});
