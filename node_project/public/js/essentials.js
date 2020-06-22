// check if the object is empty or not
function isEmpty(obj) {
    if (obj == null){
    	return true;
    }
    else if(obj == undefined){

    	return true;
    }

    return Object.keys(obj).length === 0;

}



// creating space for playlist
function create_space(){
	var playdiv = document.getElementById('playlist_area');


	// generating five items for playlist
	for(var i = 0; i < 5; i++){
		var list = document.createElement('li');
		var child_div = document.createElement('div');
		child_div.className = "song_div";

		
		// creating a heading element
		var child_head = document.createElement('input');
		child_head.className = "song_head";
		child_head.type = 'submit';
		child_head.value = 'Fetching... ';

		// styling the the heading
		child_head.style.color = "white";
		child_head.style.background= "transparent";
		child_head.style.borderStyle = 'none';
		child_head.style.fontSize= '30px';
		child_head.style.alignContent = 'center';
		child_head.style.textTransform = 'capitalize';
		child_head.style.padding = '20px';
		// creating a text node for head node
		child_div.appendChild(child_head);
		list.appendChild(child_div);
		playdiv.appendChild(list);
	}
}



// returns an  info object
async function get_song_info(song_id){
	const infoByIdUrlEndpoint = `api/getinfobyid/?id=${song_id}`;
	const res = await fetch(infoByIdUrlEndpoint);
	const songInfoObj = await res.text();
	return JSON.parse(songInfoObj);
}

function set_playList(){
	setTrackEssentials(songObjList);
}

// assigning signature
async function assign_signature(){
	songObjList = await get_play_list_from_server();
	set_playList();
	var song_heads = document.getElementsByClassName("song_head");
	if(songObjList){
		for(let i = 0; i < Math.min(songObjList.length, song_heads.length); i++){
			// adding more signature to the playlist
            song_heads[i].id = songObjList[i].id;
			song_heads[i].value = songObjList[i].title + ' ' + songObjList[i].artist;
			song_heads[i].name = songObjList[i].title
			song_heads[i].onclick = async function() { playme(songObjList[i]) };
		}
	}

}

function hightlight_in_list(curIndex){

	var all = document.getElementsByClassName("song_head");
	for(var i = 0; i < all.length; i++){
		if(i != curIndex){
			all[i].style.color = 'white';
		}
		else{
			all[i].style.color = 'yellow';
		}
	}
}



// this function will play the song
function playme(curSong){
	for(let i = 0; i < songObjList.length;i++){
		if(songObjList[i].id == curSong.id){
			currIndex = i - 1; // reference from new-player.js
			selectTrack(1); // reference from new-player.js
			hightlight_in_list(currIndex);
			break;
		}
	}
}

// a function to get the songlist from the server
async function get_play_list_from_server(){
	const playlistUrlApiEndpoint = "api/getplaylistdata";
	const res = await fetch(playlistUrlApiEndpoint);
	const playlistString = await res.text();
	const playlistIds = playlistString.split(' ').map( (id) =>{
		return parseInt(id);
	});
	const promises = []
	for( id of playlistIds){
		promises.push(get_song_info(id));
	}
	// modification code
	const songObjList = await Promise.all(promises);
	const changedList = []
	for(const song of songObjList){
	    let obj = {... song};
	    obj.artist = song.aritst;
	    delete obj.aritst;
	    changedList.push(obj)
    }
	return changedList;
}



// like change the status of the like song
async function likedAction(){
	for(let i = 0; i < songObjList.length; i++){
		if(i === currIndex){
			const curSongObj = songObjList[i];
			const res = await fetch(`api/like/?id=${curSongObj.id}`)
			console.log('liked action success');
			return
		}
	}
	console.log('error in liked action');
}

async function unlikedAction(){
	for(let i = 0; i < songObjList.length; i++){
		if(i === currIndex){
			const curSongObj = songObjList[i];
			const res = await fetch(`api/unlike/?id=${curSongObj.id}`)
			console.log('unliked action success');
			return
		}
	}
	console.log('error in unliked action');
}


var songObjList;
create_space();
assign_signature();