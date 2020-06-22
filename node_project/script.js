var mongoose = require('mongoose');
var csv = require('csv-parser');
var fs = require('fs');
mongoose.connect('mongodb://localhost:8000/test', { useMongoClient: true }, (err, next) => 
{
  if(err)
  {
    console.log(err.stack);
  }
  else
  {
    console.log('connected to database');
  }
});

var Song  = require('./models/songs.js');

fs = fs.createReadStream('music_data.csv').pipe(csv()).on('data', (row) => {
    var song = new Song();
    song.id = row.id;
    song.title = row.title;
    song.artist = row.Artist;
    song.album = row.Album;
    song.filename = row.filename;
    song.save();
}).on('end', () => {
    console.log('file complete');
});

