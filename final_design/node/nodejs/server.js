#!/usr/bin/env node

// get libraries
var util = require('util');
var fs = require('fs');
var http = require('http');
var purecss = require('purecss');
var path = require('path');

console.log(purecss.getFilePath("pure-min.css"));

// get movie info
var mp4 = 'movies/r2-d2-funny.mp4';
var new_hope = 'movies/new_hope.mp4';
// var stat = fs.statSync(mp4);
// var total = stat.size;

// read website parts
var header = fs.readFileSync('header.html');
var footer = fs.readFileSync('footer.html');
var error = fs.readFileSync('error.html');
var index = fs.readFileSync('index.html');
var video = fs.readFileSync('video.html');
var ee = fs.readFileSync('ee.html');
var compe = fs.readFileSync('compe.html');

// var path = require('path');
// var extname = String(path.extname(req.url)).toLowerCase();
// var contentType = mimeTypes[extname];
var mimeTypes = {
	'.html': 'text/html',
	'.js': 'text/javascript',
	'.css': 'text/css',
	'.json': 'application/json',
	'.png': 'image/png',
	'.jpg': 'image/jpg',
	'.gif': 'image/gif',
	'.wav': 'audio/wav',
	'.mp4': 'video/mp4',
	'.woff': 'application/font-woff',
	'.ttf': 'application/font-ttf',
	'.eot': 'application/vnd.ms-fontobject',
	'.otf': 'application/font-otf',
	'.svg': 'application/image/svg+xml'
};

// return 404 error
function sendError(res){
	res.writeHead(200, { 'Content-Type': 'text/html' });
	res.write(header);
	res.write(error);
	res.write(footer);
	res.end();
	return;
}

// return a full webpage
function sendHtml(res, body){
	res.writeHead(200, { 'Content-Type': 'text/html' });
	res.write(header);
	res.write(body);
	res.write(footer);
	res.end();
	return;
}


// create a server and setup routing
var server = http.createServer(function(req, res) {
	// console.log(req.url);

	// load the main index page
	if (req.url === '/'){
		return sendHtml(res, index);
	}
	// the following are some of the cached pages, to lower read times, but
	// honestly we aren't servering millions of pages so probably don't need
	// to do this
	else if (req.url.match(/ee/)){
		return sendHtml(res, ee);
	}
	else if (req.url.match(/video/)){
		return sendHtml(res,video);
	}
	else if (req.url.match(/compe/)){
		return sendHtml(res, compe);
	}
	// non-cached page, something someone added or whatever
	else if (req.url.match(/html/)){
		try {
			var file = fs.readFileSync('.' + req.url, 'utf-8');
			return sendHtml(res, file);
		}
		catch (err) {
			console.log(err.path);
			return sendError(res);
		}
	}
	// these handle images: jpeg, png
	else if (req.url.match(/jpg/)){
		// console.log("JPEG:" + req.url);
		try {
			var file = fs.readFileSync('.' + req.url);
			res.writeHead(200, { 'Content-Type': 'image/jpg' });
			res.end(file, "binary");
		}
		catch (err) {
			console.log(err.path);
			return sendError(res);
		}
	}
	else if (req.url.match(/png/)){
		// console.log("PNG:" + req.url);
		try {
			var file = fs.readFileSync('.' + req.url);
			res.writeHead(200, { 'Content-Type': 'image/png' });
			res.end(file, "binary");
		}
		catch (err) {
			console.log(err.path);
			return sendError(res);
		}
	}
	// Cascading Sytle Sheets (CSS)
	else if (req.url === "/pure-min.css"){
		console.log(">> serving " + req.url);
		var file = fs.readFileSync(purecss.getFilePath("pure-min.css")).toString();
		// console.log(file);
		res.writeHead(200, { 'Content-Type': 'text/css' });
		return res.end(file);
	}
	// Movies in mp4 format
	else if (req.url.match(/mp4/)){
		// req.url -> /r2-d2-funny.mp4
		// var range = req.headers.range;
		// if (!range) {
		// 	// 416 Wrong range
		// 	return res.sendStatus(416);
		// }
		// var positions = range.replace(/bytes=/, "").split("-");
		// var start = parseInt(positions[0], 10);
		// var total = stats.size;
		// var end = positions[1] ? parseInt(positions[1], 10) : total - 1;
		// var chunksize = (end - start) + 1;
		// res.writeHead(206, {
		// 	"Content-Range": "bytes " + start + "-" + end + "/" + total,
		// 	"Accept-Ranges": "bytes",
		// 	'Content-Length': total,
		// 	'Content-Type': 'video/mp4'
		// });
		// fs.createReadStream(path).pipe(res);

		// need to fix this to handle more than one movie
		var file;

		// figure out which file the user is asking for
		if (req.url.match(/new_hope/)){
			file = path.resolve(__dirname, new_hope);
		}
		else {
			file = path.resolve(__dirname, mp4);
		}
		fs.stat(file, function(err, stats) {
			if (err) {
				if (err.code === 'ENOENT') {
					// 404 Error if file not found
					// return res.sendStatus(404);
					return sendError(res);
				}
				res.end(err);
			}
			var range = req.headers.range;
			if (!range) {
				// 416 Wrong range
				// return res.sendStatus(416);
				// res.writeHead(416, { 'Content-Type': 'text/html' });
				res.writeHead(416);
				res.end();
				return;
			}
			var positions = range.replace(/bytes=/, "").split("-");
			var start = parseInt(positions[0], 10);
			var total = stats.size;
			var end = positions[1] ? parseInt(positions[1], 10) : total - 1;
			var chunksize = (end - start) + 1;

			res.writeHead(206, {
				"Content-Range": "bytes " + start + "-" + end + "/" + total,
				"Accept-Ranges": "bytes",
				"Content-Length": chunksize,
				"Content-Type": "video/mp4"
			});

			var stream = fs.createReadStream(file, { start: start, end: end })
				.on("open", function() {
					stream.pipe(res);
				}).on("error", function(err) {
					res.end(err);
				});
			});
	}
	// okay, we don't support what the user is asking for, send an error
	else {
		console.log("ERROR:" + req.url);
		return sendError(res);
	}
})

// launch server
server.listen(9000);
console.log('open http://hostname:9000');
