const express = require('express')
const firebase = require('firebase')
const bodyParser = require('body-parser')
const cors = require('cors')
const request = require('request');


// Initialize Express
const app = express()
app.use(bodyParser.json()); // for parsing application/json
app.use(cors())
app.use(express.static('web'))

// Initialize Firebase
var config = {
  apiKey: "AIzaSyBzX7gVYuZzocDLN1fdCfbVCfYYm2xTzow",
  authDomain: "thecloset-94652.firebaseapp.com",
  databaseURL: "https://thecloset-94652.firebaseio.com",
  projectId: "thecloset-94652",
  storageBucket: "thecloset-94652.appspot.com",
  messagingSenderId: "727915381699"
};
firebase.initializeApp(config);
var database = firebase.database();

var bottoms = ["jeans", "shorts"]; //types of clothing considered bottom
var tops = ["t-shirt", "jacket"]; //types of clothing considered top


// Express routing
// Gets the entire closet of clothes and parses it into a JSON array, adding the uid of the article as an attribute.
app.get('/getCloset', function(req, res) {
  var closet_array = [];

  database.ref('closet').once('value', function(closet) {
    closet.forEach(function(article) {
      var articleJSON = article.val();
      var key = article.key;
      articleJSON['uid'] = key;
      closet_array.push(articleJSON);
    });
    res.send(closet_array);
  });
})

// Takes a new article of clothing, adds the "pos" attribute, and posts it to the database.
app.post('/newArticle', function(req, res) {
  var article = req.body;
  var newPostKey = database.ref().child('closet').push().key;
  if (bottoms.indexOf(article.type) != -1) {
    article['pos'] = "bottom";
  } else if (tops.indexOf(article.type) != -1) {
    article['pos'] = "top";
  }

  database.ref('closet/' + newPostKey).set(article);

  res.sendStatus(200);
})

// Accepts the uid of an article as a query parameter and removes that article from the closet, and removes all saved outfits with that article.
app.delete('/removeArticle', function(req, res) {
      var id = req.query.uid;

      database.ref('closet/' + id).remove();

      database.ref('badOutfits').once('value', function(outfits) {
        outfits.forEach(function(outfit) {
          if (outfit.val()[0]['uid'] == id || outfit.val()[1]['uid'] == id) {
            database.ref('badOutfits/' + outfit.key).remove();
          }
        });
      });
        database.ref('goodOutfits').once('value', function(outfits) {
          outfits.forEach(function(outfit) {
            if (outfit.val()[0]['uid'] == id || outfit.val()[1]['uid'] == id) {
              database.ref('goodOutfits/' + outfit.key).remove();
            }
          });
        });

        res.sendStatus(200);
      })

      // Lexie's IP: 35.3.12.61
      // Arham: 35.3.66.193
      app.get('/getOutfits', function(req, res) {
        request({
          url: 'http://localhost:5000/getOutfits',
          method: "GET",
        }, function(error, response, body) {
          if (!error && response.statusCode == 200) {
            res.status(response.statusCode).json(body);
          } else
            {
              res.sendStatus(500);
            }
          });
      })

      // Takes a new outfit and posts it to the database, then posts it to the Flask AI.
      app.post('/likeOutfit', function(req, res) {
        var outfit = req.body;
        var newPostKey = database.ref().child('outfits').push().key;

        database.ref('goodOutfits/' + newPostKey).set(outfit);

        //35.3.12.61
        request({
          url: 'http://localhost:5000/giveGoodOutfit',
          method: "POST",
          json: outfit
        }, function(error, response, body) {
          if (!error && response.statusCode == 200) {
            res.status(response.statusCode).json(body);
          } else {
            {
              res.sendStatus(500);
            }
          }
        });
      })

      app.post('/dislikeOutfit', function(req, res) {
        var outfit = req.body;
        var newPostKey = database.ref().child('outfits').push().key;

        database.ref('badOutfits/' + newPostKey).set(outfit);

        //35.3.12.61
        request({
          url: 'http://localhost:5000/giveBadOutfit',
          method: "POST",
          json: outfit
        }, function(error, response, body) {
          if (!error && response.statusCode == 200) {
            res.status(response.statusCode).json(body);
          } else {
            {
              res.sendStatus(500);
            }
          }
        });
      })

      // The server is started.
      app.listen(process.env.PORT || 3000, function() {
        console.log('Server started at port 3000')
      })
