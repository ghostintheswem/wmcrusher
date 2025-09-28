const feed = document.getElementById('feed');
const imageCount = 12; // Adjust based on how many images you have

for (let i = 0; i < imageCount; i++) {
  const img = document.createElement('img');
  img.src = `output/2${i}output_image.png`;
  img.alt = `Post ${i}`;
  img.onerror = function () {
    this.style.display = 'none';
  };
  feed.appendChild(img);
}
