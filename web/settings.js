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

	Game.init_board( width, height, selectAI.value );
}


window.addEventListener( "DOMContentLoaded", function() {

	var buttonApply = document.getElementById( "apply" );

	inputWidth = document.getElementById( "board_width" ),
	inputHeight = document.getElementById( "board_height" );
	selectAI = document.getElementById( "ai_system" );
	buttonApply.addEventListener( "click", settings_apply, false );

	Game.MLP.weights_1 = MLP_weights_1;
	Game.MLP.weights_2 = MLP_weights_2;
	Game.RBF.weights = RBF_weights_1;
	Game.RBF.perceptron.weights = RBF_weights_2;
	Game.RBF.sigma = RBF_sigma;
	Game.DTree.tree = DTree_tree;

	Game.init_board( DEFAULT_COLS, DEFAULT_ROWS, DEFAULT_AI );

}, false );