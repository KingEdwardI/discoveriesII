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
// serve folder
var serveIndex = require('serve-index');
var requireDir = require('require-dir');
var dir = requireDir('./orders', {recurse: true});
// save html as pdf
var pdf = require('html-pdf');
var options = { "format" : "A4"}; // "base" : __dirname
// run command line programs
var exec = require('child_process').exec;


var PORT = 8000;

app.post('/uploads', type,
  (req,res,next) => {
    var uploadfile = req.file.filename; // unique identifier for uploaded file
    var finalfile = req.file.originalname; // final filename to be written
    
    var csvtojson = new csvToJson({});
    csvtojson.fromFile("./uploads/" + uploadfile, (err, result) => { // read from csv file and convert to json
      if (err) {
        return console.log('csv-to-json Failed: ', err);
      }
      
      fs.writeFile(__dirname + '/json/' + uploadfile + '.json', JSON.stringify(result), (err) => { // write converted json to new file
        if (err) {
          return console.log('writeFile Failed: ', err);
        }
        exec('python buildorder.py ./json/' + uploadfile + '.json ./orders/' + finalfile.replace('.csv', '') + '.html ./orders/' + finalfile.replace('.csv', '') + '-label.html', (err) => {
          if (err) {
            console.log('python failed: ', err);
          }
          
        });

      });

    });

    res.redirect('orders/')

});

app.use(express.static(__dirname));
app.use(express.static('orders/'));

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

app.use('/orders', serveIndex(__dirname + '/orders/', {'icons': true}));

app.listen(PORT, () => {
  console.log('listening on port: ' + PORT);
});
