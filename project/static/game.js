const gcanvas = document.getElementById("canvas-game");
gcanvas.width = window.innerWidth;
gcanvas.height = window.innerHeight;

const gc = gcanvas.getContext("2d");

const scoreEl = document.querySelector("#scoreEl");
const startGameBtn = document.querySelector("#startGameBtn");
const modalEl = document.querySelector("#modalEl");
const bigScoreEl = document.querySelector("#bigScoreEl");
const pointsEl = document.querySelector("#pointsEl");

class Player {
  constructor(x, y, radius, color) {
    this.x = x;
    this.y = y;
    this.radius = radius;
    this.color = color;
  }

  draw() {
    gc.beginPath();
    gc.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
    gc.fillStyle = this.color;
    gc.fill();
  }
}

class Projectile {
  constructor(x, y, radius, color, velocity) {
    this.x = x;
    this.y = y;
    this.radius = radius;
    this.color = color;
    this.velocity = velocity;
  }

  draw() {
    gc.beginPath();
    gc.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
    gc.fillStyle = this.color;
    gc.fill();
  }

  update() {
    this.draw();
    this.x = this.x + this.velocity.x;
    this.y = this.y + this.velocity.y;
  }
}

class Enemy {
  constructor(x, y, radius, color, velocity) {
    this.x = x;
    this.y = y;
    this.radius = radius;
    this.color = color;
    this.velocity = velocity;
  }

  draw() {
    gc.beginPath();
    gc.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
    gc.fillStyle = this.color;
    gc.fill();
  }

  update() {
    this.draw();
    this.x = this.x + this.velocity.x;
    this.y = this.y + this.velocity.y;
  }
}

const friction = 0.99;
class Particle {
  constructor(x, y, radius, color, velocity) {
    this.x = x;
    this.y = y;
    this.radius = radius;
    this.color = color;
    this.velocity = velocity;
    this.alpha = 1;
  }

  draw() {
    gc.save();
    gc.globalAlpha = this.alpha;
    gc.beginPath();
    gc.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
    gc.fillStyle = this.color;
    gc.fill();
    gc.restore();
  }

  update() {
    this.draw();
    this.velocity.x *= friction;
    this.velocity.y *= friction;
    this.x = this.x + this.velocity.x;
    this.y = this.y + this.velocity.y;
    this.alpha -= 0.01;
  }
}

const x = gcanvas.width / 2;
const y = gcanvas.height / 2;

let player = new Player(x, y, 10, "white");
let projectiles = [];
let enemies = [];
let particles = [];

function init() {
  player = new Player(x, y, 10, "white");
  projectiles = [];
  enemies = [];
  particles = [];
  score = 0;
  scoreEl.innerHTML = score;
  bigScoreEl.innerHTML = score;
}

function spawnEnemies() {
  setInterval(() => {
    const radius = Math.random() * (35 - 4) + 4;

    let x;
    let y;

    if (Math.random() < 0.5) {
      x = Math.random() < 0.5 ? 0 - radius : gcanvas.width + radius;
      y = Math.random() * gcanvas.height;
    } else {
      x = Math.random() * gcanvas.width;
      y = Math.random() < 0.5 ? 0 - radius : gcanvas.height + radius;
    }
    const color = `hsl(${Math.random() * 360}, 50%, 50%)`;

    const angle = Math.atan2(gcanvas.height / 2 - y, gcanvas.width / 2 - x);

    const velocity = {
      x: Math.cos(angle) / 3,
      y: Math.sin(angle) / 3,
    };

    enemies.push(new Enemy(x, y, radius, color, velocity));
  }, 1500);
}

let animationId;
let score = 0;
function animate() {
  animationId = requestAnimationFrame(animate);
  gc.fillStyle = "rgba(0, 0, 0, 0.15)";
  gc.fillRect(0, 0, gcanvas.width, gcanvas.height);
  player.draw();
  particles.forEach((particle, index) => {
    if (particle.alpha <= 0) {
      particles.splice(index, 1);
    } else {
      particle.update();
    }
    particle.update();
  });
  projectiles.forEach((projectile, index) => {
    projectile.update();

    //remove from edge of screen
    if (
      projectile.x + projectile.radius < 0 ||
      projectile.x - projectile.radius > gcanvas.width ||
      projectile.y + projectile.radius < 0 ||
      projectile.y - projectile.radius > gcanvas.height
    ) {
      setTimeout(() => {
        projectiles.splice(index, 1);
      }, 0);
    }
  });

  enemies.forEach((enemy, index) => {
    enemy.update();

    const dist = Math.hypot(player.x - enemy.x, player.y - enemy.y);
    //end game
    if (dist - enemy.radius - player.radius < 1) {
      cancelAnimationFrame(animationId);
      modalEl.style.display = "flex";
      bigScoreEl.innerHTML = score;
      pointsEl.innerHTML = 'Points' + '<br />' + '<br />' + '<b>Great Job!</b>';
    }

    projectiles.forEach((projectile, projectileIndex) => {
      const dist = Math.hypot(projectile.x - enemy.x, projectile.y - enemy.y);

      //when projectiles touch enemies
      if (dist - enemy.radius - projectile.radius < 1) {
        //create explosions
        for (let i = 0; i < enemy.radius * 2; i++) {
          particles.push(
            new Particle(
              projectile.x,
              projectile.y,
              Math.random() * 2,
              enemy.color,
              {
                x: (Math.random() - 0.5) * (Math.random() * 6),
                y: (Math.random() - 0.5) * (Math.random() * 6),
              }
            )
          );
        }

        if (enemy.radius - 10 > 5) {
          //increase our score
          score += 100;
          scoreEl.innerHTML = score;

          gsap.to(enemy, {
            radius: enemy.radius - 10,
          });
          setTimeout(() => {
            projectiles.splice(projectileIndex, 1);
          }, 0);
        } else {
          // remove from scene all together
          score += 250;
          scoreEl.innerHTML = score;
          setTimeout(() => {
            enemies.splice(index, 1);
            projectiles.splice(projectileIndex, 1);
          }, 0);
        }
      }
    });
  });
}

addEventListener("click", (event) => {
  const angle = Math.atan2(
    event.clientY - gcanvas.height / 2,
    event.clientX - gcanvas.width / 2
  );

  const velocity = {
    x: Math.cos(angle) * 5,
    y: Math.sin(angle) * 5,
  };

  projectiles.push(
    new Projectile(gcanvas.width / 2, gcanvas.height / 2, 5, "white", velocity)
  );
});

startGameBtn.addEventListener("click", () => {
  init();
  animate();
  spawnEnemies();
  modalEl.style.display = "none";
});
