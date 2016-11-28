function makeRecipes(recipes, moveTo) {
  for (var i in recipes) {
    var recipe = recipes[i];
    var recipeDoc = null;

    try {
      var docTitle = recipe.title || 'Untitled';
      recipeDoc = DocumentApp.create(docTitle);
      writeNewRecipeDoc(recipeDoc, recipe);
      moveFile(recipeDoc.getId(), moveTo);

    } catch (error) {
      if (recipeDoc) {
        DriveApp.getFileById(recipeDoc.getId()).setTrashed(true);
      }
      var errorsDoc = DocumentApp.create(recipe.title || 'Untitled Errors');
      var errorsBody = errorsDoc.getBody();
      errorsBody.appendParagraph(errorToVerboseString(error));
      errorsBody.appendParagraph(JSON.stringify(recipe));
      moveFile(errorsDoc.getId(), moveTo);

    }
  }
}

function writeNewRecipeDoc(recipeDoc, recipe) {
  var recipeBody = recipeDoc.getBody();

  // 0.5in * 72pts/in
  recipeBody.setMarginBottom(36);
  recipeBody.setMarginLeft(36);
  recipeBody.setMarginRight(36);
  recipeBody.setMarginTop(36);

  if (recipe.imageUrl) {
    var imageResponse = UrlFetchApp.fetch(recipe.imageUrl);
    var imageBlob = imageResponse.getBlob();
    var recipeImage = recipeBody
    .appendParagraph('')
    .setAlignment(DocumentApp.HorizontalAlignment.CENTER)
    .appendInlineImage(imageBlob);
    setImageDimensions(recipeImage);
  }

  var docTitle = recipe.title || 'Untitled';
  recipeBody.appendParagraph(docTitle).setHeading(DocumentApp.ParagraphHeading.HEADING2);
  recipeBody.appendParagraph('');

  if (recipe.extra) {
    var extraTextParagraph = recipeBody.appendParagraph('');
    extraTextParagraph.appendText(recipe.extra.join('\r'));
  }

  if (recipe.ingredients) {
    addList(recipeBody, 'Ingredients', recipe.ingredients, DocumentApp.GlyphType.BULLET);
  }

  if (recipe.instructions) {
    addList(recipeBody, 'Instructions', recipe.instructions, DocumentApp.GlyphType.NUMBER);
  }

  return recipeDoc;
}

function setImageDimensions(image) {
  var height = image.getHeight();
  var width = image.getWidth();

  var heightScalar = 650/height;
  var widthScalar = 650/width;

  var scalar = Math.min(heightScalar, widthScalar);

  image.setHeight(scalar*height);
  image.setWidth(scalar*width);
}

function addList(body, header, listItems, glyphType) {
  body.appendParagraph(header).setHeading(DocumentApp.ParagraphHeading.HEADING2);
  var itemId = null;
  for (var i in listItems) {
    if (itemId == null) {
      itemId = body.appendListItem(listItems[i]);
    } else {
      itemId = body.appendListItem(listItems[i]).setListId(itemId);
    }

    itemId.setGlyphType(glyphType);
  }
}

function moveFile(docId, targetFolderId) {
  var file = DriveApp.getFileById(docId);
  var folder = DriveApp.getFolderById(targetFolderId);
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);
}

function errorToVerboseString(error) {
  var message = error.message + ' ' + error.stack;
  return message;
}
