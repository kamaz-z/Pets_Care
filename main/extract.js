const fs = require('fs');
const path = require('path');

// Вкажи шлях до папки, з якої треба витягти текст. 
// Якщо скрипт у тій же папці — залиш '.'
const targetDir = '.'; 
const outputFile = 'all_content_windows.txt';

// Список розширень, які ми вважаємо текстовими (можеш додати свої)
const textExtensions = ['.txt', '.js', '.json', '.html', '.css', '.py', '.md', '.sql', '.env'];

function getAllFiles(dirPath, arrayOfFiles = []) {
  const files = fs.readdirSync(dirPath);

  files.forEach(function(file) {
    const fullPath = path.join(dirPath, file);
    
    // Пропускаємо системні та важкі папки
    if (['node_modules', '.git', '.idea', 'dist', 'build'].includes(file)) return;

    if (fs.statSync(fullPath).isDirectory()) {
      arrayOfFiles = getAllFiles(fullPath, arrayOfFiles);
    } else {
      // Перевіряємо, чи це текстовий файл
      if (textExtensions.includes(path.extname(file).toLowerCase()) || file.endsWith('ssh-key')) {
        arrayOfFiles.push(fullPath);
      }
    }
  });

  return arrayOfFiles;
}

try {
  console.log('--- Пошук файлів розпочато ---');
  const files = getAllFiles(targetDir);
  let finalContent = '';

  files.forEach(filePath => {
    if (filePath.endsWith(outputFile) || filePath.endsWith('extract.js')) return;
    
    const content = fs.readFileSync(filePath, 'utf8');
    finalContent += `\n\n================================================\n`;
    finalContent += `FILE: ${filePath}\n`;
    finalContent += `================================================\n\n`;
    finalContent += content;
  });

  fs.writeFileSync(outputFile, finalContent);
  console.log(`\nУспіх! Знайдено файлів: ${files.length}`);
  console.log(`Результат збережено у: ${path.resolve(outputFile)}`);
} catch (error) {
  console.error('Сталася помилка:', error.message);
}