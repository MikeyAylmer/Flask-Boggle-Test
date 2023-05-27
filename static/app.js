class BoggleGame {

    constructor(boardId, seconds = 60) {
        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardId);
        // how long game runs
        this.seconds = seconds;
        this.showTimer();
        this.timer = setInterval(this.tick.bind(this), 1000);

        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }

    showWord(word) {
        $(".words", this.board).append($("<li>", { text: word }));
    }

    showMessage(msg, cls) {
        $(".msg", this.board)
            .text(msg)
            .removeClass()
            .addClass(`msg ${cls}`);
    }

    async handleSubmit(evt) {
        evt.preventDefault();
        const $word = $(".word", this.board);

        let word = $word.val();
        if (!word) return;

        if (this.words.has(word)) {
            this.showMessage(`Already found ${word}`, "err");
            return;
        }

        const resp = await axios.get("/check-word", { params: { word: word } });
        if (resp.data.result === "not-word") {
            this.showMessage(`${word} is not a word`, "err");
        } else if (resp.data.result === "not-on-board") {
            this.showMessage(`${word} is not a word on this board`, "err");
        } else {
            this.showWord(word);
            this.score += word.length;
            this.showScore();
            this.words.add(word);
            this.showMessage(`Added: ${word}`, "ok");
        }

        $word.val("").focus();
    }

    showScore() {
        $('.score', this.board).text(this.score);
    }

    showTimer() {
        $('.timer', this.board).text(this.seconds)
    }

    async tick() {
        this.seconds -= 1;
        this.showTimer();

        if (this.seconds === 0) {
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }
}
