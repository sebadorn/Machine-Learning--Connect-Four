/**
 * Apply settings.
 */
function settings_apply() {
	width = inputWidth.value;
	height = inputHeight.value;

	if( width < 1 ) {
		width = DEFAULT_COLS;
		inputWidth.value = DEFAULT_COLS;
	}
	if( height < 1 ) {
		height = DEFAULT_ROWS;
		inputHeight.value = DEFAULT_ROWS;
	}

	Game.init_board( width, height );
}


window.addEventListener( "DOMContentLoaded", function() {

	var buttonApply = document.getElementById( "apply" );

	inputWidth = document.getElementById( "board_width" ),
	inputHeight = document.getElementById( "board_height" );
	selectANN = document.getElementById( "ann" );
	buttonApply.addEventListener( "click", settings_apply, false );

	Game.init_board( DEFAULT_COLS, DEFAULT_ROWS );

}, false );