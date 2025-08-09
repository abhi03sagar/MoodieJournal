const mongoose=require('mongoose');
const { type } = require('os');
const userSchema=new mongoose.Schema({
    username: {type: String, unique: true},
    password: String,
});

module.exports=mongoose.model('User', userSchema);