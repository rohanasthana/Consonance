var mongoose = require('mongoose');
var Schema = mongoose.Schema;

songSchema = new Schema( {
	
	id: Number,
    title: String,
    artist: String,
    album: String, 
    filename: String
}),
song = mongoose.model('song', songSchema);

module.exports = song;