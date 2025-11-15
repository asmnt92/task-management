// for admin dashboard nav_bar

  // Menu toggle
  const menuToggle = document.getElementById("menu-toggle");
  const mobileMenu = document.getElementById("mobile-menu");

  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener("click", function () {
      mobileMenu.classList.toggle("hidden");
    });
  }

  // User menu toggle
  const userMenuButton = document.getElementById("user-menu-button");
  const userMenu = document.getElementById("user-menu");

  if (userMenuButton && userMenu) {
    userMenuButton.addEventListener("click", function () {
      userMenu.classList.toggle("hidden");
    });

    // Close dropdown when clicking outside
    window.addEventListener("click", function (e) {
      if (!userMenuButton.contains(e.target)) {
        userMenu.classList.add("hidden");
      }
    });
  }

