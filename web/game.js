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
    DEFAULT_ROWS = 6;


/**
 * Game "class".
 */
var Game = {

	board: {
		gui: null,
		fields: null
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
		b.fields = new Array();
		b.gui = document.getElementById( "board" );
		while( b.gui.hasChildNodes() ) {
			b.gui.removeChild( b.gui.firstChild );
		}

		// Init game board columns and fields therein.
		for( var i = 0; i < width; i++ ) {
			b.fields[i] = new Array();
			col = Game.create_column( i, height );

			for( var j = 0; j < height; j++ ) {
				b.fields[i][j] = STONE_BLANK;
				field = Game.create_single_field( i, j );
				col.appendChild( field );
			}

			b.gui.appendChild( col );
		}
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
		column.addEventListener( "click", Game.set_stone );
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
	 * Set a stone.
	 */
	set_stone: function( event ) {
		var bf = Game.board.fields,
		    id, col,
		    i, j;

		// Get column.
		id = event.target.id;
		if( id.indexOf( "field_" ) == 0 ) {
			id = event.target.parentNode.id;
		}
		col = id.replace( "col_", "" );

		// Flatten game board in order to pass it to the AI.
		var board_flat = new Array();
		for( i = 0; i < bf.length; i++ ) {
			for( j = 0; j < bf[i].length; j++ ) {
				board_flat[board_flat.length] = bf[i][j];
			}
		}

		// Ask the AI
		out = Game.use_mlp( board_flat );
		// TODO: <out> is not what I expected. Not at all.

		console.log( out );
	},


	/**
	 * Use the trained MLP.
	 * @param {Array} inputs
	 * @return {Array} outputs
	 */
	use_mlp: function( inputs ) {
		var exp, i, j, k, hidden,
		    neuron_connections_layer1 = Game.MLP.weights_1[0].length,
		    neuron_connections_layer2 = Game.MLP.weights_2[0].length;

		// Add bias node
		inputs[inputs.length] = -1.0;

		// Activation in hidden layer
		hidden = new Array();
		for( j = 0; j < inputs.length; j++ ) {
			hidden[j] = 0.0;
			for( i = 0; i < neuron_connections_layer1; i++ ) {
				hidden[j] += inputs[i] * Game.MLP.weights_1[i][j];
			}
		}
		for( i = 0; i < hidden.length; i++ ) {
			exp = Math.exp( -1.0 * Game.MLP.beta * hidden[i] );
			hidden[i] = 1.0 / ( 1.0 + exp );
		}

		// Add bias node
		hidden[hidden.length] = -1.0;

		// Activation in output layer
		outputs = new Array();
		for( k = 0; k < hidden.length; k++ ) {
			outputs[k] = 0.0;
			for( j = 0; j < neuron_connections_layer2; j++ ) {
				hidden[k] += inputs[j] * Game.MLP.weights_2[j][k];
			}
		}
		// outputs = dotproduct( hidden, Game.MLP.weights_2 );
		for( i = 0; i < outputs.length; i++ ) {
			exp = Math.exp( -1.0 * Game.MLP.beta * outputs[i] );
			outputs[i] = 1.0 / ( 1.0 + exp );
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