// @license magnet:?xt=urn:btih:b8999bbaf509c08d127678643c515b9ab0836bae&dn=ISC.txt ISC-License
'use strict';
let Answered = 0, AnsweredCorrectly = 0;
let Total;
let AnsweredArray;

let RealTime;
let TimeLimit;

let AnsweredStatus;
let CountDown;

let End;

function Click() {
	let Node = this;

	let Question = this.name;

	if (AnsweredArray[Question])
		return;
	AnsweredArray[Question] = true;

	if (!RealTime) {
		AnsweredStatus.textContent = ++Answered + '/' + Total;
		return;
	}

	do {
		Node = Node.parentNode;
	} while (Node.nodeName != 'UL')

	let Inputs = Node.getElementsByTagName('input');
	for (let i = 0; i < Inputs.length; ++i) {
		if (RealTime)
			Inputs[i].disabled = true;
	}

	let Answer = this.value;

	let Correct = (Answers[Question] == Answer ? true : false);

	do {
		Node = Node.parentNode;
	} while (Node.nodeName != 'FIELDSET')

	Node.classList.add(Correct ? 'c' : 'w');

	Node = this;
	do {
		Node = Node.parentNode;
	} while (Node.nodeName != 'LI')

	if (Correct) {
		Node.style.fontWeight = 'bold';
		AnsweredCorrectly++;
	} else {
		Node.style.textDecoration = 'line-through';
		for (let i = 0; i < Inputs.length; ++i)
			if (Inputs[i].value == Answers[Question]) {
				Node = Inputs[i];
				do {
					Node = Node.parentNode;
				} while (Node.nodeName != 'LI')
				Node.style.fontWeight = 'bold';
				break;
			}
	}

	AnsweredStatus.textContent = AnsweredCorrectly + '/' + ++Answered + '/' + Total;

	if (Answered >= Total) {
		clearInterval();
		window.onbeforeunload = null;
		BeforePOST();
		const Form = document.getElementsByTagName('form')[0];
		Form.submit();
	}
}

function BeforePOST() {
	const Checkboxes = document.getElementsByTagName('input');
	for (let i = 0; i < Checkboxes.length; ++i) {
		let Checkbox = Checkboxes[i];
		if (Checkbox.type == 'radio') {
			Checkbox.disabled = false;
			Checkbox.onclick = function() { return false };
		}
	}
}

function Tick() {
	let Diff = End - Date.now();
	if (Diff < 1000) {
		CountDown.textContent = 'Time\'s up!';
		clearInterval();
		window.onbeforeunload = null;
		BeforePOST();
		const Form = document.getElementsByTagName('form')[0];
		Form.submit();
		return;
	}

	Diff /= 1000;

	let Hours = Diff / 60 / 60 | 0;
	let Minutes = (Diff / 60 | 0) % 60;
	if (Minutes < 10)
		Minutes = '0' + Minutes;
	let Seconds = (Diff | 0) % 60;
	if (Seconds < 10)
		Seconds = '0' + Seconds;

	CountDown.textContent = (Hours ? Hours + ':' : '') + Minutes + ':' + Seconds;
}

function OnLoad() {
	let URLO = new URL(window.location.href);
	RealTime = URLO.searchParams.get('rt');
	TimeLimit = URLO.searchParams.get('tl');

	const Inputs = document.getElementsByTagName('input');
	for (let i = 0; i < Inputs.length; ++i) {
		let Input = Inputs[i];
		if (Input.type == 'radio')
			Input.onclick = Click;
		else if (Input.type == 'submit') {
			Input.onclick = function() { window.onbeforeunload = null; };
		}
	}
	if (RealTime) {
		const Form = document.getElementsByTagName('form')[0];
		Form.addEventListener('submit', BeforePOST);
	}

	Total = document.getElementsByTagName('fieldset').length;
	AnsweredArray = [];

	const Status = document.createElement('div');
	Status.id = 'status';
	let StatusHTML = '<span>' + (RealTime ? AnsweredCorrectly + '/' : '') + Answered + '/' + Total + '</span>'

	if (TimeLimit)
		StatusHTML += ' &mdash; <span><span>'

	Status.innerHTML = '<p>' + StatusHTML + '</p>'

	AnsweredStatus = Status.firstChild.firstChild;

	if (TimeLimit) {
		CountDown = Status.firstChild.lastChild;
		CountDown.textContent = '2:00:00';
		End = Date.now() + 2 * 60 * 60 * 1000;
		setInterval(Tick, 1000);
	}

	document.body.appendChild(Status);
}

// Here be spoilers!
const Answers =
[2,2,1,2,0,0,3,0,0,3,1,2,0,0,1,0,3,3,2,1,3,2,2,2,1,1,3,2,3,0,3,0,2,3,1,2,0,1,3,0,2,1,3,0,1,3,1,1,1,2,1,0,3,3,0,0,2,1,2,3,2,1,2,1,0,2,3,1,2,1,3,1,1,2,3,2,3,1,0,3,2,0,0,1,0,0,1,3,2,2,3,2,2,0,1,1,0,0,2,1,0,3,2,0,1,3,1,3,2,3,3,3,2,3,0,0,1,2,1,2,2,0,1,0,1,3,3,0,1,1,0,1,3,3,0,3,3,3,3,0,0,3,1,2,2,0,3,0,2,0,0,1,3,2,0,3,3,1,0,2,2,0,3,2,0,1,1,2,2,0,2,0,1,2,1,3,0,0,3,1,1,0,1,0,3,2,1,3,2,0,0,1,3,1,3,2,2,3,3,1,0,0,3,0,0,0,3,1,0,1,1,2,0,0,1,1,0,2,1,1,3,1,0,1,0,1,0,1,2,1,1,3,0,2,3,0,2,3,1,2,2,3,1,1,2,1,1,1,0,3,2,1,0,3,2,3,0,3,2,1,0,1,2,2,1,3,0,2,0,2,3,2,2,3,1,2,0,2,1,1,1,3,0,2,0,3,0,1,0,2,2,0,2,1,3,3,1,2,1,2,0,2,0,1,1,0,3,1,1,2,0,2,1,2,2,3,2,3,3,3,0,0,3,2,1,1,2,2,1,3,2,0,0,3,1,2,0,2,2,1,2,1,2,2,1,3,0,2,1,0,0,3,1,2,3,0,1,2,2,1,0,2,2,3,0,0,3,1,0,2,1,2,3,3,1,2,3,1,2,0,3,1,1,0,0,1,3,2,1,2,1,3,0,0,3,3,1,1,2,3,1,3,2,0,2,3,0,2,2,3,0,1,0,1,1,3,0,1,0,1,1,2,2,0,0,3,2,0,3,1,2,0,1,2,3,0,1,2,3,0,2,1,3,3,0,1,0,1,0,1,2,2,3,1,1,2,2,3,2,0,0,0,2,3,0,0,2,0,3,3,0,1,2,2,3,0,2,3,2,1,1,2,1,3,0,1,3,3,3,0,0,1,0,0,1,0,2,1,1,1,2,1,1,2,1,2,3,3,1,0,1,2,1,3,3,0,2,2,1,2,0,0,2,2,3,0,3,1,3,3,3,3,3,0,2,1,0,3,1,1,1,1,0,2,2,2,3,3,3,1,0,3,1,0,2,2,1,2,0,1,1,2,0,3,1,2,3,1,3,0,0,1,3,1,2,1,2,0,0,3,1,2,2,1,3,1,0,0,2,3,0,2,3,3,2,0,1,1,0,2];

window.onload = OnLoad;
window.onbeforeunload = function () {
	if (Answered)
		return 'Are you sure you want to lose your progress?';
};
// @license-end
