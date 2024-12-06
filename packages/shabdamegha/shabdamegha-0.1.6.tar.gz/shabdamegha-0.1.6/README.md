# Shabdamegha
![shabdamegha](https://sbissoyi.github.io/shabdamegha/docs/shabdamegha.png)

`Shabdamegha` is a python library to generate word cloud for Odia language with proper rendering of Ligatures (Yuktakshars). (ଯୁକ୍ତାକ୍ଷର ଗୁଡ଼ିକୁ ସଠିକ୍‌ ପ୍ରଦର୍ଶିତ କରି ଶବ୍ଦମେଘ ସୃଷ୍ଟି କରିବା ନିମନ୍ତେ ଏକ ପାଇଥନ୍‌ ଲାଇବ୍ରେରୀ)

## Features
- Support for Yuktakshar rendering.
- Flexible customization of font, color, orientation, and placement.
- Expandable canvas for dynamic word placement.

## Installation
```bash
pip install shabdamegha

## Usage
from shabdamegha.shabdamegha import draw_shabdamegha

# Example usage
districts_of_odisha = {
                        "ଅନୁଗୋଳ": 13, "କଟକ": 8, "କଳାହାଣ୍ଡି": 16, "କନ୍ଧମାଳ": 16, "କେନ୍ଦୁଝର": 17, "କେନ୍ଦ୍ରାପଡ଼ା": 5, "କୋରାପୁଟ": 18, "ଖୋର୍ଦ୍ଧା": 6,
                        "ଗଜପତି": 8, "ଗଞ୍ଜାମ": 16, "ଜଗତସିଂହପୁର": 4, "ଝାରସୁଗୁଡ଼ା": 4, "ଢେଙ୍କାନାଳ": 9, "ଦେବଗଡ଼": 6, "ନବରଙ୍ଗପୁର": 11, "ନୟାଗଡ଼": 8,
                        "ନୂଆପଡ଼ା": 8, "ପୁରୀ": 6, "ବରଗଡ଼": 12, "ବଲାଙ୍ଗୀର": 13, "ବାଲେଶ୍ୱର": 7, "ବୌଦ୍ଧ": 7, "ଭଦ୍ରକ": 5, "ମୟୂରଭଞ୍ଜ": 21, "ମାଲକାନଗିରି": 12,
                        "ଯାଜପୁର": 6, "ରାୟଗଡ଼ା": 14, "ସମ୍ବଲପୁର": 13, "ସୁବର୍ଣ୍ଣପୁର": 5, "ସୁନ୍ଦରଗଡ଼": 19
                        }
draw_shabdamegha(districts_of_odisha, colors=[(148, 0, 211), (0, 0, 255), (5, 108, 8), (255, 127, 0), (255, 0, 0)])

draw_shabdamegha(
    data="ଶ୍ରୀଜଗନ୍ନାଥ ଓଡ଼ିଶା ଦୁର୍ଗାପୂଜା କଟକ ପୁରୀ ଭୁବନେଶ୍ୱର ନବରଙ୍ଗପୁର କୋରାପୁଟ ମୟୂରଭଞ୍ଜ",
    save_file_path="example_wordcloud.png",
    orientations=[-90, -60, -30, 0, 30, 60, 90]
    )

words = ["ଶ୍ଳେଷ", "ସନ୍ନିବେଶ", "ଶୃଙ୍ଖଳା", "ଚାଞ୍ଛିବା", "ଝୁଣ୍ଟିଆ", "ରୋମନ୍ଥନ", "କୁମ୍ଭୀର", "ବାଗ୍ଦେବୀ", "କଚ୍ଛପ", "ଖଡ୍ଗଧାରି", "ଅକ୍ଷୁର୍ଣ୍ଣ", "ଉଡ୍ଡୀୟମାନ", "ଉତ୍କଣ୍ଠା", "ସମ୍ଭତ୍ସର", "ଉଦ୍ଘାଟନ", "ଉଦ୍ଦେଶ୍ୟ", "ଉଦ୍ଧାର", "ମୁଦ୍ଗର", "ଅଦ୍ଭୁତ", "ପିପ୍ପଳୀ", "ଅପ୍ସରା", "କୁବ୍ଜ", "ତିବ୍ବତ", "ସମ୍ମାନ", "ବଳ୍କଳ", "ଫାଲ୍ଗୁନ", "ସଂକଳ୍ପ", " ବଲ୍ଲଭ", "ଶିରଶ୍ଛେଦ", "ନିଷ୍ପୀଡନ", "ମାହାତ୍ମ୍ୟ", "ନିର୍ଦ୍ଧାରିତ", "ପଶ୍ଚିମ", "ପରିଷ୍କାର", "ଆସ୍ଫାଳନ", "ସମ୍ପ୍ରଦାନ", "ନିଷ୍ପ୍ରୟୋଜନ"]
draw_shabdamegha(words, font_file_paths=['C:/Windows/Fonts/Kalinga.ttf', 'C:/Windows/Fonts/nirmala.ttc'], colors=True)
