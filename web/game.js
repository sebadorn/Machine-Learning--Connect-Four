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
			col = document.createElement( "div" );
			col.setAttribute( "class", "column" );
			col.setAttribute( "id", "col_" + i );
			col.style.width = FIELD_WIDTH + "px";
			col.style.height = ( FIELD_HEIGHT * height ) + "px";

			for( var j = 0; j < height; j++ ) {
				b.fields[i][j] = STONE_BLANK;
				field = document.createElement( "span" );
				field.setAttribute( "class", "field blank" );
				field.setAttribute( "id", "field_" + i + "-" + j );
				field.style.width = FIELD_WIDTH + "px";
				field.style.height = FIELD_HEIGHT + "px";
				field.style.bottom = ( j * FIELD_HEIGHT ) + "px";
				col.appendChild( field );
			}

			b.gui.appendChild( col );
		}
	},


	/**
	 * Set a stone.
	 * @param {int} x
	 * @param {int} y
	 * @param {float} stone
	 */
	set_stone: function( x, y, stone ) {
		// TODO
	}

};