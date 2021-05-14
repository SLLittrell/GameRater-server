SELECT * FROM raterprojectapi_game
SELECT * FROM raterprojectapi_review
DROP TABLE IF EXISTS Review

CREATE TABLE "raterprojectapi_review" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "title" TEXT,
    "review" TEXT,
    "game_id"INTEGER,
    "reviewer_id" INTEGER DEFAULT NULL,
    FOREIGN KEY(`reviewer_id`) REFERENCES `Player`(`id`),
    FOREIGN KEY(`game_id`) REFERENCES `Game`(`id`)
)