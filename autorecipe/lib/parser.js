'use strict';

var sentenceCase = function (paragraph) {
  var sentences = paragraph.split('. ');
  var sentencesCased = sentences.map(function (sentence) {
    return sentence[0].toUpperCase() + sentence.slice(1).toLowerCase();
  });
  var paragraphCased = sentencesCased.join('. ');
  return paragraphCased;
};

var parseRecipe = function (recipeLines) {
  var recipe = {};

  var currentSection = 'title';
  recipeLines.map(function (line) {
    var trimmedLine = line.trim();

    if (trimmedLine.toLowerCase() === 'ingredients') {
      currentSection = 'ingredients';

    } else if (['instructions', 'directions'].indexOf(trimmedLine.toLowerCase()) !== -1) {
      currentSection = 'instructions';

    } else if (trimmedLine.length === 0) {
      currentSection = 'extra';

    } else if (currentSection === 'title') {
      recipe.title = trimmedLine;
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
