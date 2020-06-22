var express = require('express');
var router = express.Router();
var User = require('../models/user');
var Song = require('../models/songs');
var request = require('request');
const spawn = require('child_process').spawn
let path = require('path');
const fs = require('fs');

router.get('/register', function (req, res, next) {
	if(req.session && req.session.userId)
	{
		res.redirect('/profile')
	}

	return res.render('register.ejs');
});


router.post('/register', function(req, res, next) {
	console.log(req.body);
	var personInfo = req.body;


	if(!personInfo.email || !personInfo.username || !personInfo.password || !personInfo.passwordConf){
		res.send();
	} else {
		if (personInfo.password == personInfo.passwordConf) {

			User.findOne({email:personInfo.email},function(err,data){
				if(!data){
					var c;
					User.findOne({},function(err,data){

						if (data) {
							console.log("if");
							c = data.unique_id + 1;
						}else{
							c=1;
						}

						var newPerson = new User({
							unique_id:c,
							email:personInfo.email,
							username: personInfo.username,
							password: personInfo.password,
							passwordConf: personInfo.passwordConf
						});

						newPerson.save(function(err, Person){
							if(err)
								console.log(err);
							else
								console.log('Success');
						});

					}).sort({_id: -1}).limit(1);
					res.send({"Success":"You are regestered,You can login now."});
				}else{
					res.send({"Success":"Email is already used."});
				}

			});
		}else{
			res.send({"Success":"password is not matched"});
		}
	}
});

router.get('/login', function (req, res, next) {
	if(req.session && req.session.userId) {
		return res.redirect('/profile');
	}
	return res.render('login.ejs');
});

router.post('/login', function (req, res, next) {
	//console.log(req.body);
	User.findOne({email:req.body.email},function(err,data){
		if(data){
			
			if(data.password==req.body.password){
				//console.log("Done Login");
				req.session.userId = data.unique_id;
				//console.log(req.session.userId)
				res.send({"Success":"Success!"});
				
			}else{
				res.send({"Success":"Wrong password!"});
			}
		}else{
			res.send({"Success":"This Email Is not regestered!"});
		}
	});
});

router.get('/profile', function (req, res, next) {
	console.log("profile");
	User.findOne({unique_id:req.session.userId},function(err,data){
		console.log("data");
		console.log(data);
		if(!data){
			res.redirect('/login');
		}else{
			//console.log("found");
			return res.render('profile.ejs', {"name":data.username,"email":data.email});
		}

	});


});

router.get('/logout', function (req, res, next) {
	console.log("logout")
	if (req.session) {
    // delete session object
    req.session.destroy(function (err) {
    	if (err) {
    		return next(err);
    	} else {
    		return res.redirect('/login');
    	}
    });
}
});

router.get('/forgetpass', function (req, res, next) {
	res.render("forget.ejs");
});

router.post('/forgetpass', function (req, res, next) {
	//console.log('req.body');
	//console.log(req.body);
	User.findOne({email:req.body.email},function(err,data){
		console.log(data);
		if(!data){
			res.send({"Success":"This Email Is not regestered!"});
		}else{
			// res.send({"Success":"Success!"});
			if (req.body.password==req.body.passwordConf) {
			data.password=req.body.password;
			data.passwordConf=req.body.passwordConf;

			data.save(function(err, Person){
				if(err)
					console.log(err);
				else
					console.log('Success');
					res.send({"Success":"Password changed!"});
			});
		}else{
			res.send({"Success":"Password does not matched! Both Password should be same."});
		}
		}
	});
	
});

// API for web music player

router.get('/api/getinfobyid', function(req, res, next){ // DONE
	var ID = parseInt(req.query.id);
	console.log("backend id ",ID);
	console.log('get info by id ' + ID);
	Song.findOne({id: ID}, function(err, item)
	{
		console.log(item);
		if(!item)
		{
			res.json({'message':'No song found with this id'});
		}
		else
		{	
			console.log(item);
			res.json({'id':item.id, 'aritst': item.artist, 'album': item.album, 'filename': item.filename, 'title':item.title});
		}

	});
	
});

router.get('/api/like', function(req, res, next){
	var ID = req.query.id;
	var userID = req.session.userId;
	console.log(`Like song of id ${ID} by user ${userID}`);
	User.findOne({unique_id: userID},  (err, user) => {
		if(!user)
		{
			res.json({"message":"User not found"});
		}
		else
		{
			if(user.liked_songs.includes(ID) === false)
			{
				user.liked_songs.push(ID);
			}
			res.json({"message": "done"});
			user.save();
		}
	});
});

router.get('/api/unlike', function(req, res, next){
	var ID = req.query.id;
	var userID = req.session.userId;
	console.log(`Unlike song of id ${ID} by user ${userID}`);
	User.findOne({unique_id: userID},  (err, user) => {
		if(!user)
		{
			res.json({"message":"User not found"});
		}
		else
		{
			if(user.liked_songs.includes(ID) === true)
			{
				var ind = user.liked_songs.indexOf(ID);
				user.liked_songs.splice(ind, 1);
			}
			res.json({"message": "done"});
			user.save();
		}
	});
});

router.get('/api/getplaylistdata', async function(req, res, next){
	var ID = req.query.id;
	var userID = req.session.userId;
	console.log(`getting playlist for user ${userID}`);
	await User.findOne({unique_id: userID},  async (err, user) => {
		if(!user)
		{
			res.json({"message":"User not found"});
		}
		else
		{
			
			var str = String();
			for(var i = 0 ; i < user.liked_songs.length; i++){
				if(i)
				{
					str += ' ';
				}
				str += user.liked_songs[i];
			}
				await request({
			    method: 'POST',
			    url: 'http://localhost:5000',
			    type: 'application/json',
			    form: {'song':str},
			    json: true
			  },
			  function (error, response, body) {
			    if (error) {
			      return console.error('upload failed:', error);
			    }
				res.send(response.body);

			  });
		// res.send("1 2 3 4 5");
		}
	});
});

router.get('/api/fileAcess', function(req, res, next){
	const { fileName } = req.query;
	const rootPath = process.cwd() + '/files/'
	const pathname = rootPath + fileName;
	var filestream = fs.createReadStream(pathname);

	filestream.on('open', function() {
		var stats = fs.statSync(pathname);
		var fileSizeInBytes = stats["size"];
		var bytes_start =0;
		var bytes_end = fileSizeInBytes;

		var chunk_size = bytes_end - bytes_start;

		if (chunk_size == fileSizeInBytes) {
			// Serve the whole file as before
			res.writeHead(200, {
				"Accept-Ranges": "bytes",
				'Content-Type': 'audio/mpeg',
				'Content-Length': fileSizeInBytes});
			filestream.pipe(res);
		} else {
			// HTTP/1.1 206 is the partial content response code
			res.writeHead(206, {
				"Content-Range": "bytes " + bytes_start + "-" + bytes_end + "/" + fileSizeInBytes,
				"Accept-Ranges": "bytes",
				'Content-Type': 'audio/mpeg',
				'Content-Length': fileSizeInBytes
			});
			filestream.pipe(res);
		}
	});
});


module.exports = router;