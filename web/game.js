// Constants (more or less, I mean, this is JavaScript, so ...)

var STONE_BLANK = 0.0,
    STONE_HUMAN = 1.0,
    STONE_AI = -1.0,
    WIN = 0.0,
    DRAW = 0.5,
    LOSS = 1.0,
    ANN_MLP = "mlp",
    ANN_RBF = "rbf";

var FIELD_WIDTH = 60, // [px]
    FIELD_HEIGHT = 60, // [px]
    DEFAULT_COLS = 7,
    DEFAULT_ROWS = 6,
    CONNECT = 4;


/**
 * Game "class".
 */
var Game = {

	count_ai_moves: 0,
	last_move_human: 0,
	ended: false,

	board: {
		gui: null,
		fields: null,
		col_heights: null
	},

	MLP: {
		beta: 1.0,
		weights_1: null,
		weights_2: null
	},

	RBF: {},

	DTree: {},


	/**
	 * Initialise game board.
	 * @param {int} width Number of columns.
	 * @param {int} height Number of rows.
	 */
	init_board: function( width, height ) {
		var b = Game.board; // shortcut variable
		var col, field;

		// Reset game board
		Game.ended = false;
		Game.count_ai_moves = 0;
		b.fields = new Array();
		b.col_heights = new Array();
		b.gui = document.getElementById( "board" );
		while( b.gui.hasChildNodes() ) {
			b.gui.removeChild( b.gui.firstChild );
		}

		// Init game board columns and fields therein.
		for( var i = 0; i < width; i++ ) {
			b.fields[i] = new Array();
			b.col_heights[i] = 0;
			col = Game.create_column( i, height );

			for( var j = 0; j < height; j++ ) {
				b.fields[i][j] = STONE_BLANK;
				field = Game.create_single_field( i, j );
				col.appendChild( field );
			}

			b.gui.appendChild( col );
		}

		Game.set_msg( "Game ready! Human player begins. <em>(That’s you.)</em>" );
	},


	/**
	 * Create a column.
	 */
	create_column: function( col, height ) {
		var column = document.createElement( "div" );
		column.setAttribute( "class", "column" );
		column.setAttribute( "id", "col_" + col );
		column.style.width = FIELD_WIDTH + "px";
		column.style.height = ( FIELD_HEIGHT * height ) + "px";
		column.addEventListener( "click", Game.choose_column );
		return column;
	},


	/**
	 * Create a single field for inside a column.
	 */
	create_single_field: function( col, row ) {
		var field = document.createElement( "span" );
		field.setAttribute( "class", "field blank" );
		field.setAttribute( "id", "field_" + col + "-" + row );
		field.style.width = FIELD_WIDTH + "px";
		field.style.height = FIELD_HEIGHT + "px";
		field.style.bottom = ( row * FIELD_HEIGHT ) + "px";
		return field;
	},


	/**
	 * Display a message on the page.
	 */
	set_msg: function( msg ) {
		var msg_area = document.getElementById( "msg" );
		msg_area.innerHTML = msg;
	},


	/**
	 * Human player chooses a column.
	 */
	choose_column: function( event ) {
		var bf = Game.board.fields, // shortcut variable
			board_flat, id, col, i, j,
			ai_use_col, winner;

		// Get column.
		id = event.target.id;
		if( id.indexOf( "field_" ) == 0 ) {
			id = event.target.parentNode.id;
		}
		col = id.replace( "col_", "" );

		// Place stone of human player
		Game.set_stone( col, STONE_HUMAN );

		// Check for winner
		winner = Game.check_win();
		if( winner == STONE_HUMAN ) {
			Game.set_msg( "Winner: Human!" );
			return;
		}
		else if( winner == STONE_AI ) {
			Game.set_msg( "Winner: AI!" );
			return;
		}

		// Draw
		if( Game.check_board_full() ) {
			Game.set_msg( "No more free fields. It's a draw!" );
			return;
		}

		// Flatten game board in order to pass it to the AI.
		board_flat = Game.flatten( bf );

		// Forced move or not
		ai_use_col = Game.find_forced_move();
		// Not forced, then ask the AI
		if( ai_use_col < 0 ) {
			ai_use_col = Game.ask_ai();
		}
		// Place stone of AI
		Game.set_stone( ai_use_col, STONE_AI );

		// Check for winner
		winner = Game.check_win();
		if( winner == STONE_HUMAN ) {
			Game.set_msg( "Winner: Human!" );
			return;
		}
		else if( winner == STONE_AI ) {
			Game.set_msg( "Winner: AI!" );
			return;
		}

		// Draw
		if( Game.check_board_full() ) {
			Game.set_msg( "No more free fields. It's a draw!" );
			return;
		}
	},


	/**
	 * Set stone in a column.
	 */
	set_stone: function( col, stone ) {
		var b = Game.board, // shortcut variable
		    row = b.col_heights[col],
		    gui_stone;

		b.fields[col][row] = stone;
		b.col_heights[col]++;

		gui_stone = document.getElementById( "field_" + col + "-" + row );
		if( stone == STONE_HUMAN ) {
			gui_stone.setAttribute( "class", "field human" );
			Game.last_move_human = col;
		}
		else {
			gui_stone.setAttribute( "class", "field ai" );
			Game.set_msg( "AI chooses column " + ( col + 1 ) + "." );
			Game.count_ai_moves++;
		}
	},


	/**
	 * Flatten a 2-dimensional array.
	 */
	flatten: function( board ) {
		var board_flat = new Array();
		for( i = 0; i < board.length; i++ ) {
			for( j = 0; j < board[i].length; j++ ) {
				board_flat[board_flat.length] = board[i][j];
			}
		}
		return board_flat;
	},


	/**
	 * Create a deepcopy of a 2-dimensional array.
	 */
	deepcopy: function( copyme ) {
		var i, thecopy = new Array();

		for( i = 0; i < copyme.length; i++ ) {
			thecopy[i] = copyme[i].slice();
		}

		return thecopy;
	},


	/**
	 * Compares the value of the found stone with the existing stone types.
	 * Sets a stop flag if it is not possible anymore for either the human or the AI
	 * to connect enough stones.
	 * Returns a tuple in the form: ( position of a blank field, #ai, #human, flag_to_stop ).
	 */
	count_stones: function( column, row, stone, blank, ai, human ) {
		var result = {
				"blank": blank, "ai": ai, "human": human,
				"flag_stop": false
			};

		if( stone == STONE_BLANK ) {
			// No danger/chance if there is more than one blank field in range
			if( result["blank"] != -1 ) { result["flag_stop"] = true; }
			// Save blank field. This is a candidate to place the stone.
			else { result["blank"] = { "col": column, "row": row }; }
		}
		else if( stone == STONE_AI ) {
			// If there has been at least one human stone already,
			// it is not possible for AI stones to have a connection of three and a blank field available.
			if( result["human"] > 0 ) { result["flag_stop"] = true; }
			else { result["ai"] += 1; }
		}
		else if( stone == STONE_HUMAN ) {
			// Same here, vice versa.
			if( result["ai"] > 0 ) { result["flag_stop"] = true; }
			else { result["human"] += 1; }
		}

		return result;
	},


	/**
	 * From position (x,y) count the types of the next stones upwards.
	 */
	count_stones_up: function( x, y ) {
		var r = { "blank": -1, "ai": 0, "human": 0 },
		    stone, i, col, row;

		if( y + CONNECT <= Game.board.fields[0].length ) {
			for( i = 0; i < CONNECT; i++ ) {
				col = x;
				row = y + i;
				stone = Game.board.fields[col][row];
				r = Game.count_stones(
					col, row, stone, r["blank"], r["ai"], r["human"]
				);
				if( r["flag_stop"] == true ) { break; }
			}
		}

		return r;
	},


	/**
	 * From position (x,y) count the types of the next stones to the right.
	 */
	count_stones_right: function( x, y ) {
		var r = { "blank": -1, "ai": 0, "human": 0 },
		    stone, i, col, row;

		if( x + CONNECT <= Game.board.fields.length ) {
			for( i = 0; i < CONNECT; i++ ) {
				col = x + i;
				row = y;
				stone = Game.board.fields[col][row];
				r = Game.count_stones(
					col, row, stone, r["blank"], r["ai"], r["human"]
				);
				if( r["flag_stop"] == true ) { break; }
			}
		}

		return r;
	},


	/**
	 * From position (x,y) count the types of the next stones diagonal right up.
	 */
	count_stones_rightup: function( x, y ) {
		var r = { "blank": -1, "ai": 0, "human": 0 },
		    stone, i, col, row,
		    width = Game.board.fields.length,
		    height = Game.board.fields[0].length;

		if( x + CONNECT <= width && y + CONNECT <= height ) {
			for( i = 0; i < CONNECT; i++ ) {
				col = x + i;
				row = y + i;
				stone = Game.board.fields[col][row];
				r = Game.count_stones(
					col, row, stone, r["blank"], r["ai"], r["human"]
				);
				if( r["flag_stop"] == true ) { break; }
			}
		}

		return r;
	},


	/**
	 * From position (x,y) count the types of the next stones diagonal right down.
	 */
	count_stones_rightdown: function( x, y ) {
		var r = { "blank": -1, "ai": 0, "human": 0 },
		    stone, i, col, row;

		if( x + CONNECT <= Game.board.fields.length && y - CONNECT + 1 >= 0 ) {
			for( i = 0; i < CONNECT; i++ ) {
				col = x + i;
				row = y - i;
				stone = Game.board.fields[col][row];
				r = Game.count_stones(
					col, row, stone, r["blank"], r["ai"], r["human"]
				);
				if( r["flag_stop"] == true ) { break; }
			}
		}

		return r;
	},


	/**
	 * Check the game board if someone has won.
	 * Returns the stone value of the winner or
	 * the value of a blank stone if there is no winner yet.
	 */
	check_win: function() {
		var b = Game.board, // shortcut
		    x, y, r;

		for( x = 0; x < b.fields.length; x++ ) {
			for( y = 0; y < b.fields[x].length; y++ ) {
				// We only care about players, not blank fields
				if( b.fields[x][y] == STONE_BLANK ) { continue; }

				// Check: UP
				r = Game.count_stones_up( x, y );
				if( r["ai"] == CONNECT ) { return STONE_AI; }
				else if( r["human"] == CONNECT ) { return STONE_HUMAN; }

				// Check: RIGHT
				r = Game.count_stones_right( x, y );
				if( r["ai"] == CONNECT ) { return STONE_AI; }
				else if( r["human"] == CONNECT ) { return STONE_HUMAN; }

				// Check: DIAGONAL RIGHT UP
				r = Game.count_stones_rightup( x, y );
				if( r["ai"] == CONNECT ) { return STONE_AI; }
				else if( r["human"] == CONNECT ) { return STONE_HUMAN; }

				// Check: DIAGONAL RIGHT DOWN
				r = Game.count_stones_rightdown( x, y );
				if( r["ai"] == CONNECT ) { return STONE_AI; }
				else if( r["human"] == CONNECT ) { return STONE_HUMAN; }
			}
		}

		return STONE_BLANK;
	},


	/**
	 * Returns true if there are no more free fields, false otherwise.
	 */
	check_board_full: function() {
		var b = Game.board, // shortcut
		    i;

		for( i = 0; i < b.fields.length; i++ ) {
			if( b.fields[i].indexOf( STONE_BLANK ) != -1 ) {
				return false;
			}
		}
		return true;
	},


	/**
	 * Check if it is possible to place a stone in the given field.
	 * Returns True if possible, False otherwise.
	 */
	check_proposed_col: function( pos ) {
		var b = Game.board; // shortcut

		if( pos == -1 ) {
			return false;
		}

		if( pos["col"] >= 0 && pos["col"] < b.fields.length ) {
			// Check if it is possible to place the stone at the needed height
			if( pos["row"] == 0 || b.fields[pos["col"]][pos["row"] - 1] != STONE_BLANK ) {
				return true;
			}
		}

		return false;
	},


	/**
	 * Check if the next move is a forced one and where to place the stone.
	 * A forced move occurs if the human player or the AI could win the game with the next move.
	 * Returns the position where to place the stone or -1 if not necessary.
	 */
	find_forced_move: function() {
		var b = Game.board, // shortcut
		    force_x = -1,
		    x, y, r;

		for( x = 0; x < b.fields.length; x++ ) {
			for( y = 0; y < b.fields[x].length; y++ ) {
				// Check: UP
				r = Game.count_stones_up( x, y );
				// Evaluate: UP
				if( r["blank"] != -1 ) {
					// If there is a chance to win: Do it!
					if( r["ai"] == 3 ) {
						return r["blank"]["col"];
					}
					// Remember dangerous situation for now.
					// Maybe there will be a chance to win somewhere else!
					else if( r["human"] == 3 ) {
						force_x = r["blank"]["col"];
					}
				}

				// Check: RIGHT
				r = Game.count_stones_right( x, y );
				// Evaluate: RIGHT
				if( Game.check_proposed_col( r["blank"] ) ) {
					if( r["ai"] == 3 ) {
						return r["blank"]["col"];
					}
					else if( r["human"] == 3 ) {
						force_x = r["blank"]["col"];
					}
				}

				// Check: DIAGONAL RIGHT UP
				r = Game.count_stones_rightup( x, y );
				// Evaluate: DIAGONAL RIGHT UP
				if( Game.check_proposed_col( r["blank"] ) ) {
					if( r["ai"] == 3 ) { return r["blank"]["col"]; }
					else if( r["human"] == 3 ) {
						force_x = r["blank"]["col"];
					}
				}

				// Check: DIAGONAL RIGHT DOWN
				r = Game.count_stones_rightdown( x, y );
				// Evaluate: DIAGONAL RIGHT DOWN
				if( Game.check_proposed_col( r["blank"] ) ) {
					if( r["ai"] == 3 ) { return r["blank"]["col"]; }
					else if( r["human"] == 3 ) {
						force_x = r["blank"]["col"];
					}
				}
			}
		}

		return force_x;
	},


	/**
	 * Ask AI where to place the next stone.
	 */
	ask_ai: function() {
		var b = Game.board, // shortcut
		    cols = b.fields.length,
		    rows = b.fields[0].length,
		    board_copy, ai_board_format, ai_output,
		    x, y, diff_loss, diff_win, diff_draw,
		    use_pos;

		// Place AI stone
		// ("opp" as in "opponent")
		var opp_win = { "col": -1, "diff": 100.0 },
		    opp_draw = { "col": -1, "diff": 100.0 },
		    opp_loss = { "col": -1, "diff": 100.0 };

		for( x = 0; x < cols; x++ ) {
			// Cell (y) in this column (x) we are currently testing
			y = b.col_heights[x];
			if( y >= rows) { continue; }

			// The MLP AI has a bad habit to mimik the human player if he/she
			// chooses the column 3, 4 or 5 as first two moves. Which basically
			// means the AI can only loose. Stop the AI from doing that!
			if( Game.count_ai_moves == 0 && x == Game.last_move_human ) {
				continue;
			}

			// Don't change the real game board
			board_copy = Game.deepcopy( b.fields );
			board_copy[x][y] = STONE_AI;

			// Array format for the AI: 7x6 -> 1x42
			ai_board_format = Game.flatten( board_copy );

			// Get the possible outcome
			ai_output = Game.use_mlp( ai_board_format )[0];

			// Difference between targets and output
			diff_loss = LOSS - ai_output;
			diff_win = WIN - ai_output;
			diff_draw = DRAW - ai_output;
			if( diff_loss < 0.0 ) { diff_loss *= -1; }
			if( diff_win < 0.0 ) { diff_win *= -1; }
			if( diff_draw < 0.0 ) { diff_draw *= -1; }

			// Close to (opponents) LOSS
			if( diff_loss <= diff_draw) {
				if( diff_loss < opp_loss["diff"] ) {
					opp_loss["col"] = x;
					opp_loss["diff"] = diff_loss;
				}
			}

			// Close to DRAW
			else { // diff_draw <= diff_loss
				if( diff_draw < opp_draw["diff"] ) {
					opp_draw["col"] = x;
					opp_draw["diff"] = diff_draw;
				}
			}

			// Don't even check for the (opponents) WIN case.
			// Rather take the least worse DRAW column.

			console.log( [x, ai_output] );
		}
		console.log( "" );

		// We want the opponent to loose
		if( opp_loss["col"] >= 0 ) {
			use_pos = opp_loss["col"];
		}
		// If that is not possible, at least go for a draw
		else if( opp_draw["col"] >= 0 ) {
			use_pos = opp_draw["col"];
		}
		// Ugh, fine, if there is no other choice
		else if( opp_win["col"] >= 0 ) {
			use_pos = opp_win["col"];
		}
		else {
			Game.set_msg(
				"-- The AI has no idea what to do and stares mindlessly at a cloud outside the window.<br />" +
				"-- The cloud looks like a rabbit riding a pony.<br />" +
				"-- You win by forfeit."
			);
		}

		return use_pos;
	},


	/**
	 * Use the trained MLP.
	 * @param {Array} inputs
	 * @return {Array} outputs
	 */
	use_mlp: function( inputs ) {
		var exp, i, j, k, hidden, weight,
		    neuron_connections_layer1 = Game.MLP.weights_1[0].length,
		    neuron_connections_layer2 = Game.MLP.weights_2[0].length;

		// Add bias node
		inputs[inputs.length] = -1.0;

		// Activation in hidden layer
		hidden = new Array();
		for( j = 0; j < neuron_connections_layer1; j++ ) {
			hidden[j] = 0.0;
			for( i = 0; i < inputs.length; i++ ) {
				if( i < Game.MLP.weights_1.length ) {
					weight = Game.MLP.weights_1[i][j];
				}
				else {
					weight = 0.5;
				}
				hidden[j] += inputs[i] * weight;
			}
		}
		for( i = 0; i < hidden.length; i++ ) {
			exp = Math.exp( -1.0 * Game.MLP.beta * hidden[i] );
			hidden[i] = 1.0 / ( 1.0 + exp );
		}

		// Add bias node
		hidden[hidden.length] = -1.0;

		// Activation in output layer (linear)
		outputs = new Array();
		for( k = 0; k < neuron_connections_layer2; k++ ) {
			outputs[k] = 0.0;
			for( j = 0; j < hidden.length; j++ ) {
				if( j < Game.MLP.weights_2.length ) {
					weight = Game.MLP.weights_2[j][k];
				}
				else {
					weight = 0.5;
				}
				outputs[k] += hidden[j] * weight;
			}
		}

		return outputs;
	},


	/**
	 * Use the trained RBF.
	 * @param {Array} inputs
	 * @return {Array} outputs
	 */
	use_rbf: function( inputs ) {
		// TODO
	},


	/**
	 * Use the trained DTree.
	 * @param {Array} inputs
	 * @return {Array} outputs
	 */
	use_dtree: function( inputs ) {
		// TODO
	}

};