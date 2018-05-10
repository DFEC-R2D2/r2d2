#!/usr/bin/env node

// get libraries
var util = require('util');
var fs = require('fs');
var http = require('http');
var purecss = require('purecss');
var path = require('path');

console.log(purecss.getFilePath("pure-min.css"));

// get movie info
var mp4 = 'r2-d2-funny.mp4';
// var stat = fs.statSync(mp4);
// var total = stat.size;

// read website parts
var header = fs.readFileSync('header.html');
var footer = fs.readFileSync('footer.html');
var error = fs.readFileSync('error.html');

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
	console.log(req.url);
	if (req.url === '/'){
		var file = fs.readFileSync('pure.html');
		res.writeHead(200, { 'Content-Type': 'text/html' });
		return sendHtml(res, file);
	}
	else if (req.url === "/data.html"){
		res.writeHead(200, { 'Content-Type': 'text/html' });
		var file = fs.readFileSync('.' + req.url, 'utf-8');
		// console.log(">> data.html");
		// make some fake data
		var chartData = [];
		for (var i = 0; i < 5; i++){
			chartData.push(Math.random() * 50);
		}
		var page = file.replace('{{chartData}}', JSON.stringify(chartData));
		// console.log('page \n' + page);
		return sendHtml(res, page);
	}
	else if (req.url.match(/html/)){
		// the req.url will be something like: /awesome.html
		// if the file can't be found, return error
		try {
			res.writeHead(200, { 'Content-Type': 'text/html' });
			var file = fs.readFileSync('.' + req.url, 'utf-8');
			// console.log('file \n' + file);

			// if (req.url === "/data.html"){
			// 	// console.log(">> data.html");
			// 	// make some fake data
			// 	var chartData = [];
			// 	for (var i = 0; i < 20; i++){
			// 		chartData.push(Math.random() * 50);
			// 	}
			// 	var page = file.replace('{{chartData}}', JSON.stringify(chartData));
			// 	// console.log('page \n' + page);
			// 	return sendHtml(res, page);
			// }
			return sendHtml(res, file);
		}
		catch (err) {
			console.log(err.path);
			return sendError(res);
		}
	}
	else if (req.url === "moment-with-locales.min.js"){
			var file = fs.readFileSync("./node_modules/moment/min" + req.url);
			// console.log(file.toString());
			res.writeHead(200, { 'Content-Type': 'text/javascript' });
			return res.end(file.toString());
	}
	else if (req.url === "/Chart.bundle.js"){
		console.log(">> serving " + req.url);
		var file = fs.readFileSync("./node_modules/chart.js/dist" + req.url).toString();
		// console.log(file);
		res.writeHead(200, { 'Content-Type': 'text/javascript' });
		return res.end(file);
	}
	else if (req.url === "/pure-min.css"){
		console.log(">> serving " + req.url);
		var file = fs.readFileSync(purecss.getFilePath("pure-min.css")).toString();
		// console.log(file);
		res.writeHead(200, { 'Content-Type': 'text/css' });
		return res.end(file);
	}
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
		var file = path.resolve(__dirname,mp4);
		fs.stat(file, function(err, stats) {
			if (err) {
				if (err.code === 'ENOENT') {
					// 404 Error if file not found
					return res.sendStatus(404);
				}
				res.end(err);
			}
			var range = req.headers.range;
			if (!range) {
				// 416 Wrong range
				return res.sendStatus(416);
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
	else {
		console.log(req.url);
		return sendError(res);
	}
})

// launch server
server.listen(9000);
console.log('open http://hostname:9000');
