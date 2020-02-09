# How to batch resize

```
sudo apt install imagemagick
identify *.jpeg
for x in *.jpeg; do echo convert $x -resize 256 ${x%.jpeg}-small.jpeg; done
```

Piper to `sh -x` once confirmed.
