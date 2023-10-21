function deck_crea(){

	// create a array of 150 numbers which represents the cards of the game
	let deck = [];
	for(let i = -1; i < 13 ; i++){
		for(let j = 0; j < 10 ; j++){
			deck.push(i);
		}
	}
	for(let i = -2 ; i < 1 ; i++){
		if(i !== -1){
			for(let j = 0; j < 5; j++){
				deck.push(i);
			}
		}
	}

	// shuffle the array
	deck.sort(() => Math.random() -0.5);

	return deck;
}


function partage(deck, p_nb) {

	// separate the cards in the selected numbers of players and return the remaining cards and the separated cards
	let deck_p = [];
	for (var i = 0; i < p_nb; i++) {
		deck_p.push([]);
		for (var j = 0; j < 12; j++) {
			deck_p[i].push(deck.shift());
		}
	}
	return [deck_p, deck];
}

function generateTable(nb_player) {

	// display the players hand
	for(let h = 0; h < nb_player; h++){

		// create the element "table"
		const tbl = document.createElement("table");
		tbl.id = "t"+h;
		let comp = 0;
		if(h==0){
			tbl.classList.add("c_p");
		}

		for (let i = 0; i < 3; i++) {

			// create a row
			const row = document.createElement("tr");

			for (let j = 0; j < 4; j++) {

				// create a cell, which contain a button
				const cell = document.createElement("td");
				const bton = document.createElement("button");
				const btext = document.createTextNode(" ");
				let command = "card_button("+comp+", "+h+")";

				// set the attribute of the button
				bton.classList.add("bton");
				bton.setAttribute("onclick", command);
				bton.id = "b"+comp;

				// desactivate all the buttons which are not own by the first player
				if(h != 0){
					bton.setAttribute("disabled", "disabled");
				}
				
				bton.appendChild(btext);
				cell.appendChild(bton);
				row.appendChild(cell);
				comp++
			}
			tbl.appendChild(row);
		}	
		document.getElementById("game").appendChild(tbl);
	}
}

function verif_ligne(joueur) {

	// ...
	let tt = []
	let nb_id = []
	let deck_size = deck_p[joueur].length
	for (let i = 0; i < (deck_size / 3); i++) {
		tt.push([])
  		for (let h = i; h < deck_size; h += (deck_size / 3)) {
    		tt[i].push(deck_p[joueur][h]);
  		}
	}
	for (let i = 0; i < tt.length; i++) {
		let comp = 0
		if(tt[i][0] == tt[i][1] && tt[i][1] == tt[i][2]){
			for (let j = i; j < deck_size; j += (deck_size / 3)) {
				if(nb_id.length < 3 && !(document.getElementById("t"+joueur).querySelector("#b"+j).innerHTML == " ")){
					nb_id.push(j - comp);
				comp++
				}
			}
		}
	}
	if(nb_id.length == 3){
		for (let i = 0; i < nb_id.length; i++) {
			defausse.unshift(deck_p[joueur].splice(nb_id[i], 1)[0])
			document.getElementById("defausse").innerHTML = "defausse : "+defausse[0];
			elem = document.getElementById("t"+joueur).querySelector("#b"+(nb_id[i]+i));
			elem.removeAttribute("onclick")
			elem.style.backgroundColor = "darkred";
			elem.id = "delet"
		}
        elements = document.getElementById("t"+joueur).querySelectorAll('[id^="b"]');
        elements.forEach((element, index) => {
            element.id = 'b' + index;
            element.setAttribute("onclick", "card_button("+index+", "+joueur+")");
        });
	}
}

function swap_pdd(nb, joueur){

	// swap the card from the "pioche" to the player hand and from the player hand to the "defausse"
	selec_button = ""
	let tmp = deck_p[joueur][nb];
	deck_p[joueur][nb] = pioche.shift();
	defausse.unshift(tmp);

	// update the cards
	document.getElementById("t"+joueur).querySelector("#b"+nb).innerHTML = deck_p[joueur][nb];
	document.getElementById("defausse").innerHTML = "defausse : "+defausse[0];
	document.getElementById("pioche").innerHTML = "pioche : "+pioche[0];

	verif_ligne(joueur)
	verif_end(joueur)
	next_p()
}

function swap_dd(nb, joueur){

	// swap a card from the "defausse" to the player hand
	selec_button = ""
	let tmp = deck_p[joueur][nb];
	deck_p[joueur][nb] = defausse.shift();
	defausse.unshift(tmp);

	// update the cards
	document.getElementById("t"+joueur).querySelector("#b"+nb).innerHTML = deck_p[joueur][nb];
	document.getElementById("defausse").innerHTML = "defausse : "+defausse[0];

	verif_ligne(joueur)
	verif_end(joueur)
	next_p()
}

function swap_pd(nb, joueur){

	// swap the card in "pioche" to the "defausse" and reveal the card the player clicked on
	// if the card was aldready reveal, it do nothing
	selec_button = ""
	if(document.getElementById("t"+joueur).querySelector("#b"+nb).innerHTML == " "){
		defausse.unshift(pioche.shift());

		// update the cards
		document.getElementById("t"+joueur).querySelector("#b"+nb).innerHTML = deck_p[joueur][nb];
		document.getElementById("defausse").innerHTML = "defausse : "+defausse[0];
		document.getElementById("pioche").innerHTML = "pioche : "+pioche[0];

		verif_ligne(joueur)
		verif_end(joueur)
		next_p()
	}
}

function card_button(card, tab) {

	// choose which move to use depending of which button the player selected
	if (selec_button == "pioche" && !(first_start[0])){
		swap_pdd(card, tab);
	} else if (selec_button == "defausse" && !(first_start[0])){
		swap_dd(card, tab);
	} else {
		swap_pd(card, tab);
	}
}

function next_p() {
	if(first_start[0] == true){
		if((first_start.length - 1) < deck_p.length){
			first_start.push([0]);
		}
		let tmp = parseInt(c_player[1]) + 1;
		if(first_start[tmp][0] < 1){
			first_start[tmp][0] += 1;
			return;
		}
		if(deck_p.length - 1 <= parseInt(c_player[1])){
			first_start[0] = false;
		}
	}
	// desativate the buttons of the current player
	document.getElementById(c_player).classList.remove("c_p");
	for(let i = 0; i < deck_p[parseInt(c_player[1])].length; i++){
		document.getElementById(c_player).querySelector("#b"+i).setAttribute("disabled", "disabled");
	}

	// if the current player is the last player
	if (deck_p.length - 1 <= parseInt(c_player[1]) && game_end == true){
		end();
		return;
	}
	if (deck_p.length - 1 <= parseInt(c_player[1])) {
		c_player = "t0";
	} else {
		c_player = "t"+(parseInt(c_player[1], 10)+1);
	}

	// ativate the buttons of the next player
	document.getElementById(c_player).classList.add("c_p");
	for(let i = 0; i < deck_p[parseInt(c_player[1])].length; i++){
		document.getElementById(c_player).querySelector("#b"+i).removeAttribute("disabled");
	}
}

function verif_end(joueur) {
	if(deck_p[0].length > 0){
		for(let i = 0; i < deck_p[joueur].length; i++){
			if(document.getElementById("t"+joueur).querySelector("#b"+i).innerHTML == " "){
				return;
			}
		}
	}
	game_end = true;
	if(last_p == 10){
		last_p = joueur;
	}
}

function end() {
	let kill_game = false
	for (let i = 0; i < deck_p.length; i++) {
		if(score.length < deck_p.length){
			score.push([0]);
		}
		for (var j = 0; j < deck_p[i].length; j++) {
			score[i][0] = score[i][0] + deck_p[i][j];
		}
	}
	let gagnant = 999;
	for (let i = 0; i < score.length; i++){
		if(score[i] < gagnant){
			gagnant = i;
		}
		if (score[i] >= 100){
			kill_game = true;
		}
	}
	console.log(score[last_p][0]+" -> "+score[last_p][0]*2);
	score[last_p][0] *= 2;
	document.getElementById("game").remove();
	let game = document.createElement("div");
	let txt = document.createElement("p");
	let tbl = document.createElement("table");
	let cell_start = document.createElement("td");
	cell_start.classList.add("end_tab_td")
	let text_start = document.createTextNode("");
	let row = document.createElement("tr");
	cell_start.appendChild(text_start);
	row.appendChild(cell_start);
	for (let i = 0; i < score.length; i++) {
		let cell = document.createElement("td");
		cell.classList.add("end_tab_td")
		let text = document.createTextNode("Joueur "+(i+1));
		cell.appendChild(text);
		row.appendChild(cell);
	}
	tbl.appendChild(row);
	cell_start = document.createElement("td");
	cell_start.classList.add("end_tab_td")
	text_start = document.createTextNode("Score");
	row = document.createElement("tr");
	cell_start.appendChild(text_start);
	row.appendChild(cell_start);
	for (let j = 0; j < score.length; j++) {
		let cell = document.createElement("td");
		cell.classList.add("end_tab_td")
		let text = document.createTextNode(score[j]);
		cell.appendChild(text);
		row.appendChild(cell);
	}
	tbl.appendChild(row);
	tbl.id = "fin_tab";
	game.id = "game";
	if(kill_game){
		txt.innerHTML = "Fin de la partie !\nLe joueur "+(gagnant+1)+" a gagné !";
		game.appendChild(txt);
		game.appendChild(tbl);
	} else {
		txt.innerHTML = "Fin de la manche !\nLe joueur "+(gagnant+1)+" a gagné !";
		const next = document.createElement("button");
		next.innerHTML = "Suivant ->";
		next.setAttribute("onclick", "main("+deck_p.length+")");
		game.appendChild(txt);
		game.appendChild(tbl);
		game.appendChild(next);
	}
	document.body.appendChild(game);
}

function start(){
	window.score = [];
	if(document.getElementById("Train").checked == true){main(1)}
	if(document.getElementById("Deux").checked == true){main(2)}
	if(document.getElementById("Trois").checked == true){main(3)}
	if(document.getElementById("Quatre").checked == true){main(4)}
}

function main(nb_player){

	// if a game is already active, we delet it
	if(document.getElementById("game") != null){
		document.getElementById('game').remove();
	}

	let [tmp_deck, p_tmp] = partage(deck_crea(), nb_player);

	// global var
	window.first_start = [true];
	window.pioche = p_tmp;
	window.defausse = [pioche.shift()];
	window.deck_p = tmp_deck;
	window.selec_button = "";
	window.c_player = "t0";
	window.game_end = false;
	window.last_p = 10;

	// create news elements
	let table = document.createElement("div");
	let pio_def_div = document.createElement("div");
	let pioche_place = document.createElement("button");
	let defausse_place = document.createElement("button");

	// setup elements
	pioche_place.id = "pioche";
	defausse_place.id = "defausse";
	table.id = "game";
	pio_def_div.classList.add("pio_def");
	pioche_place.innerHTML = "pioche : "+pioche[0];
	defausse_place.innerHTML = "defausse : "+defausse[0];
	pioche_place.setAttribute("onclick", "selec_button = 'pioche'");
	defausse_place.setAttribute("onclick", "selec_button = 'defausse'");

	// add "game" to the main HTML and create the players cards
	document.body.appendChild(table);
	generateTable(nb_player);

	// append the remaining elements to "game"
	pio_def_div.appendChild(pioche_place);
	pio_def_div.appendChild(defausse_place);
	table.appendChild(pio_def_div);

}
