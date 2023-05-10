String toTitleCase(String text) {
  return text.toLowerCase().split(' ').map((word) {
    if (word.isEmpty) {
      return '';
    }
    return word[0].toUpperCase() + word.substring(1);
  }).join(' ');
}