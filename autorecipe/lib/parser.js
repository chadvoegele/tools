'use strict';

var titleCase = function (sentence) {
  return makeCase(sentence, ' ');
};

var sentenceCase = function (paragraph) {
  return makeCase(paragraph, '. ');
};

var makeCase = function (text, separator) {
  var splitText = text.split(separator);
  var textCased = splitText.map(function (text) {
    return text[0].toUpperCase() + text.slice(1).toLowerCase();
  });
  var joinedTextCased = textCased.join(separator);
  return joinedTextCased;
};

var parseRecipe = function (recipeLines) {
  var recipe = {};

  var currentSection = 'title';
  recipeLines.map(function (line) {
    var trimmedLine = line.trim();

    if (trimmedLine.toLowerCase().replace(/\W/g, '') === 'ingredients') {
      currentSection = 'ingredients';

    } else if (
      [ 'instructions', 'directions', 'preparation' ].some(function (w) {
        return trimmedLine.toLowerCase().replace(/\W/g, '').includes(w);
      })
    ) {
      currentSection = 'instructions';

    } else if (trimmedLine.length === 0) {
      currentSection = 'extra';

    } else if (currentSection === 'title') {
      recipe.title = titleCase(trimmedLine);
      currentSection = 'extra';

    } else if (
      ['jpg', 'png', 'gif']
      .map(function (ext) { return trimmedLine.search(ext) })
      .some(function (index) { return index >= 0; })) {
      recipe.imageUrl = trimmedLine;
      currentSection = 'extra';

    } else if (['extra', 'ingredients', 'instructions'].indexOf(currentSection) !== -1) {
      if (!recipe[currentSection]) {
        recipe[currentSection] = [];
      }
      recipe[currentSection].push(sentenceCase(trimmedLine));
    }
  });

  return recipe;
};

module.exports = parseRecipe;
