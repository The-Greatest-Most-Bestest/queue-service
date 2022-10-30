// let item = document.getElementsByName('id').value;
// console.log(item);

// let lname = document.getElementsByid('name').value;
// console.log(lname);

// let uid = document.getElementsByid('uid').value;
// console.log(uid);

// let email = document.getElementsByid('email').value;
// console.log(email);

// let phone = document.getElementsByid('phone').value;
// console.log(phone);

// let form = document.getElementById('joinWaitlist');
// console.log(form);

const express = require('express');
const app = express();
app.listen(3000, () => console.log('listening at 3000'));
app.use(express.static('public'));

app.post('/api', (request, response) => {
	console.log(request.body);
});
