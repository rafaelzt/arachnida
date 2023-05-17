# 🕷️ Spider Image Scraper 🌐

Spider is a fun and powerful tool that allows you to extract all the images from a website recursively by just providing a URL as a parameter. It's like having your personal web crawler! 🕸️

## 🚀 Usage

To use Spider, just provide a URL like this:

```bash
./spider [-rlp] URL
```

🛠️ Options

Spider provides the following options to customize your image scraping:

    -r : Enables recursive downloading of images from the provided URL. 
    This means Spider will follow all links and download images from them as well! 🔄

    -r -l [N] : Specifies the maximum depth level for recursive downloading. 
    If not provided, the default depth is 5 levels. 📏

    -p [PATH] : Specifies the path where the downloaded files will be saved. 
    If not provided, the default path is ./data/. 📁

📸 Image Formats

By default, Spider will download images with the following extensions:

    .jpg/jpeg
    .png
    .gif
    .bmp

So you'll get a wide variety of images! 🌈

🎉 Start Scraping!

Now that you know how to use Spider, start scraping and enjoy the images you find! Remember, with great power comes great responsibility, so always respect the rules and policies of the websites you scrape. 🕷

📝 License

This project is licensed under the MIT License. Feel free to use and modify the code as you like!
