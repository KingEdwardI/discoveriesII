// express
var express = require('express');
var app = express();
// bodyParser
var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
// file system
var fs = require('file-system');
// multer options for uploads
var multer = require('multer');
var upload = multer({ dest: 'uploads/' });
var type = upload.single('sampleFile');
// csv to json converter
var csvToJson = require("csvtojson").Converter;
var csvtojson = new csvToJson({});
// serve folder
var serveIndex = require('serve-index');
var requireDir = require('require-dir');
var dir = requireDir('./orders', {recurse: true});
// save html as pdf
var pdf = require('html-pdf');
var options = { "format" : "A4" };
// run command line programs
var exec = require('child_process').exec;

var PORT = 8000;

app.post('/uploads', type,
  (req,res,next) => {
    var uploadfile = req.file.filename; // unique identifier for uploaded file
    var finalfile = req.file.filename; // final filename to be written
    
    csvtojson.fromFile("./uploads/" + uploadfile, (err, result) => { // read from csv file and convert to json
      
      fs.writeFile(__dirname + '/json/' + uploadfile + '.json', JSON.stringify(result), (err) => { // write converted json to new file
        if (err) {
          return console.log(err);
        }
        exec('buildorder.py ./json/' + uploadfile + '.json ./orders/' + finalfile + '/.pdf')

        html = fs.readFileSync('./tmp/' + uploadfile + '/.html', 'utf8');
        pdf.create(html, options).toFile(__dirname + '/orders/' + req.file.originalname, (err,res) => {
          if (err) {
            return console.log(err);
          }
          res.redirect('orders/')
        })
      });

    });
    // res.redirect('/orders');
});

/*
 * function getDateTime() {
 * 
 *     var date = new Date();
 * 
 *     var hour = date.getHours();
 *     hour = (hour < 10 ? "0" : "") + hour;
 * 
 *     var year = date.getFullYear();
 * 
 *     var month = date.getMonth() + 1;
 *     month = (month < 10 ? "0" : "") + month;
 * 
 *     var day  = date.getDate();
 *     day = (day < 10 ? "0" : "") + day;
 * 
 *     return year + ":" + month + ":" + day + ":" + hour;
 * 
 * }
 */

app.use(express.static(__dirname));
app.use(express.static('orders/'));

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

app.use('/orders', serveIndex(__dirname + '/orders/', {'icons': true}));

app.listen(PORT, () => {
  console.log('listening on port: ' + PORT);
});
