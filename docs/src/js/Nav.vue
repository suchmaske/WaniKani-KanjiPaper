<template>

  <nav class="nav">
    <div class="nav-left">
      <router-link to="/" class="nav-item" exact>
          WKKP
      </router-link>
    </div>

    <div class="nav-center">
      <a class="nav-item" href="https://github.com/suchmaske/WaniKani-KanjiPaper" target="_blank">
        <span class="icon">
          <i class="fa fa-github"></i>
        </span>
      </a>
    </div>

    <!-- This "nav-toggle" hamburger menu is only visible on mobile -->
    <!-- You need JavaScript to toggle the "is-active" class on "nav-menu" -->
    <span class="nav-toggle">
      <span></span>
      <span></span>
      <span></span>
    </span>

    <!-- This "nav-menu" is hidden on mobile -->
    <!-- Add the modifier "is-active" to display it on mobile -->
    <div class="nav-right nav-menu">
      <router-link to="/kanji" class="nav-item" exact>
          Kanji Sheets
      </router-link>
      <router-link to="/vocabulary" class="nav-item" exact>
          Vocabulary Sheets
      </router-link>

      <div class="nav-item">
        <div class="field is-grouped">
          <p class="control">
            <a class="button is-primary" href="./dist/pdf/WK-Kanji-All.zip">
              <span class="icon">
                <i class="fa fa-download"></i>
              </span>
              <span>Download</span>
            </a>
          </p>
        </div>
      </div>
    </div>
  </nav>

</template>

<script>

</script>