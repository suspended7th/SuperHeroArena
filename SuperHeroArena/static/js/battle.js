window.onload = function() {
	function sleep(ms) {
		return new Promise(resolve => setTimeout(resolve, ms));
	}
	
	function random_int_from_interval(min, max) { // min and max included 
		return Math.floor(Math.random() * (max - min + 1) + min);
	}
	
	let player_roll_space = document.getElementsByClassName("player-roll-space")[0];
	let enemy_roll_space = document.getElementsByClassName("enemy-roll-space")[0];
	
	function roll_player(){
		let roll = random_int_from_interval(0, 100);
		player_roll_space.innerHTML = roll.toString();
		return roll;
	}
	function roll_enemy(){
		let roll = random_int_from_interval(0, 100);
		enemy_roll_space.innerHTML = roll.toString();
		return roll;
	}
	
	function clear_rolls(){
		player_roll_space.innerHTML = "";
		enemy_roll_space.innerHTML = "";
	}
	
	let player_hp_bar = document.getElementsByClassName("progress-bar-player")[0];
	let enemy_hp_bar = document.getElementsByClassName("progress-bar-enemy")[0];
	
	let player_hp_percent = document.getElementsByClassName("health-percent-player")[0];
	let enemy_hp_percent = document.getElementsByClassName("health-percent-enemy")[0];	
	
	let enemy_name = document.getElementsByClassName("enemy-name")[0].value;
	
	let player_inteligence = parseInt(document.getElementsByClassName("intelligence")[0].value);
	let player_strength = parseInt(document.getElementsByClassName("strength")[0].value);
	let player_speed = parseInt(document.getElementsByClassName("speed")[0].value);
	let player_durability = parseInt(document.getElementsByClassName("durability")[0].value);
	let player_power = parseInt(document.getElementsByClassName("power")[0].value);
	let player_combat = parseInt(document.getElementsByClassName("combat")[0].value);
	
	let enemy_inteligence = parseInt(document.getElementsByClassName("enemy-intelligence")[0].value);
	let enemy_strength = parseInt(document.getElementsByClassName("enemy-strength")[0].value);
	let enemy_speed = parseInt(document.getElementsByClassName("enemy-speed")[0].value);
	let enemy_durability = parseInt(document.getElementsByClassName("enemy-durability")[0].value);
	let enemy_power = parseInt(document.getElementsByClassName("enemy-power")[0].value);
	let enemy_combat = parseInt(document.getElementsByClassName("enemy-combat")[0].value);
	
	let select_inteligence = document.getElementById("intelligence");
	let select_strength = document.getElementById("strength");
	let select_speed = document.getElementById("speed");
	let select_durability = document.getElementById("durability");
	let select_power = document.getElementById("power");
	let select_combat = document.getElementById("combat");
	
	select_inteligence.addEventListener("click", check_one);
	select_strength.addEventListener("click", check_one);
	select_speed.addEventListener("click", check_one);
	select_durability.addEventListener("click", check_one);
	select_power.addEventListener("click", check_one);
	select_combat.addEventListener("click", check_one);
	
	let attack_button = document.getElementsByClassName("attack")[0];
	
	function check_one(){
		if (this.checked){
			select_inteligence.checked = false;
			select_strength.checked = false; 
			select_speed.checked = false;
			select_durability.checked = false;
			select_power.checked = false;
			select_combat.checked = false;
			this.checked = true;
			attack_button.disabled = false;
		} else {
			attack_button.disabled = true;
		}
	}
	
	attack_button.addEventListener("click", async function() {
		this.disabled = true;
		
		select_inteligence.disabled = true;
		select_strength.disabled = true;
		select_speed.disabled = true;
		select_durability.disabled = true;
		select_power.disabled = true;
		select_combat.disabled = true;
		
		let disabled_checkbox = select_inteligence;
		
		let player_mod = 0;
		let enemy_mod = 0;
		
		if (select_inteligence.checked) {
			player_mod = player_inteligence;
			enemy_mod = enemy_inteligence;
			select_inteligence.checked = false;
			disabled_checkbox = select_inteligence;
		} else if (select_strength.checked) {
			player_mod = player_strength;
			enemy_mod = enemy_strength;
			select_strength.checked = false;
			disabled_checkbox = select_strength;
		}else if (select_speed.checked) {
			player_mod = player_speed;
			enemy_mod = enemy_speed;
			select_speed.checked = false;
			disabled_checkbox = select_speed;
		}else if (select_durability.checked) {
			player_mod = player_durability;
			enemy_mod = enemy_durability;
			select_durability.checked = false;
			disabled_checkbox = select_durability;
		}else if (select_power.checked) {
			player_mod = player_power;
			enemy_mod = enemy_power;
			select_power.checked = false;
			disabled_checkbox = select_power;
		}else if (select_combat.checked) {
			player_mod = player_combat;
			enemy_mod = enemy_combat;
			select_combat.checked = false;
			disabled_checkbox = select_combat;
		}
		
		select_inteligence.checked = false;
		select_strength.checked = false;
		select_speed.checked = false;
		select_durability.checked = false;
		select_power.checked = false;
		select_combat.checked = false;
		
		let i = 100;
		let player_roll = 0;
		let enemy_roll = 0;
		while (i <= 1600){
			player_roll = roll_player();
			enemy_roll = roll_enemy();
			await sleep(i);
			i = i * 2;
		}
		player_roll += player_mod;
		enemy_roll += enemy_mod;
		
		function deal_damage(damage, hp_bar, hp_percent){
			let hp = parseInt(hp_bar.getAttribute('aria-valuenow'));
			let max_hp = parseInt(hp_bar.getAttribute('aria-valuemax'));
			
			hp -= damage;
			if (hp < 0){
				hp = 0;
			}
			let hp_per = Math.ceil(hp / max_hp * 100);
			if (hp_per > 50) {
				hp_bar.classList.remove("progress-bar-warning");
				hp_bar.classList.remove("progress-bar-danger");
				hp_bar.classList.add("progress-bar-success");
			} else if (hp_per < 50 && hp_per > 10) {
				hp_bar.classList.remove("progress-bar-success");
				hp_bar.classList.remove("progress-bar-danger");
				hp_bar.classList.add("progress-bar-warning");
			} else {
				hp_bar.classList.remove("progress-bar-success");
				hp_bar.classList.remove("progress-bar-warning");
				hp_bar.classList.add("progress-bar-danger");
			}
			hp_bar.setAttribute('aria-valuenow', hp.toString());
			hp_bar.style.width = hp_per.toString() + "%";
			hp_percent.innerHTML = hp_per.toString() + "%";
			return hp;
		}
		let hp = 0;
		if (player_roll > enemy_roll){
			let damage = player_roll - enemy_roll;
			hp = deal_damage(damage, enemy_hp_bar, enemy_hp_percent);
			alert("You dealt " + damage.toString() + " damage to " + enemy_name);
			if (hp == 0){
				alert("You have defeated " + enemy_name + "!");
			}
		} else if (player_roll < enemy_roll) {
			let damage = enemy_roll - player_roll;
			hp = deal_damage(damage, player_hp_bar, player_hp_percent);
			alert("You took " + damage.toString() + " damage.");
			if (hp == 0){
				alert("You have been defeated!");
			}
		}
		
		clear_rolls();
		if (hp != 0){
			select_inteligence.disabled = false;
			select_strength.disabled = false;
			select_speed.disabled = false;
			select_durability.disabled = false;
			select_power.disabled = false;
			select_combat.disabled = false;
			disabled_checkbox.disabled = true;
			this.disabled = true;
		} else {
			select_inteligence.disabled = true;
			select_strength.disabled = true;
			select_speed.disabled = true;
			select_durability.disabled = true;
			select_power.disabled = true;
			select_combat.disabled = true;
			let player_hp = player_hp_bar.getAttribute('aria-valuenow');
			if (player_hp > 0) {
				let new_score = document.getElementById("next_score").value;
				document.getElementById("current_score").value = new_score;
				document.getElementById("score_display").innerHTML = new_score;
			}
			document.getElementById("hp").value = player_hp;
			document.getElementById("battle_again").style.display = "block";
		}
	})
}
 