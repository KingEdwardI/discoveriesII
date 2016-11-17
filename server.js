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
var options = { "format" : "A4" }

var PORT = 8000;

app.post('/uploads', type,
  (req,res,next) => {
    // unique identifier for uploaded file
    uploadfile = req.file.filename
    // read from csv file and convert to json
    csvtojson.fromFile("./uploads/" + uploadfile, (err, result) => {
      // write converted json to new file
      fs.writeFile(__dirname + '/json/' + uploadfile + '.json', JSON.stringify(result), (err) => {
        if (err) {
          return console.log(err);
        }
        // make the html file here and place in tmp/

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

app.use(express.static(__dirname));
app.use(express.static('orders/'));

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

app.use('/orders', serveIndex(__dirname + '/orders/', {'icons': true}));

app.listen(PORT, () => {
  console.log('listening on port: ' + PORT);
});
