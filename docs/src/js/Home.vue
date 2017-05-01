<template>

    <div class="columns">


        <div class="column">
            <div class="card">
              <div class="card-content">
                <p class="title">
                  Kanji
                </p>
                <p class="subtitle">
                  All Levels
                </p>
              </div>
              <footer class="card-footer">
                <p class="card-footer-item">
                  <a href="./dist/pdf/WK-Kanji-All.zip">
                    Download (65M)
                  </a>
                </p>
                  <p class="card-footer-item">
                      <a href="./dist/pdf/WK-Kanji-1.pdf" target="_blank">
                          Example
                      </a>
                  </p>
                <p class="card-footer-item">
                    <router-link to="/kanji" exact>
                        <a>Select By Level</a>
                    </router-link>
                </p>
              </footer>
            </div>
        </div>

        <div class="column">
            <div class="card">
              <div class="card-content">
                <p class="title">
                  Vocabulary
                </p>
                <p class="subtitle">
                  All Levels
                </p>
              </div>
              <footer class="card-footer">
                <p class="card-footer-item">
                  <a href="./dist/pdf/WK-Vocab-All.zip">
                      Download (4M)
                  </a>
                </p>
                  <p class="card-footer-item">
                      <a href="./dist/pdf/WK-Vocab-1.pdf" target="_blank">
                          Example
                      </a>
                  </p>
                <p class="card-footer-item">
                    <router-link to="/vocabulary" exact>
                        <a>Select By Level</a>
                    </router-link>
                </p>
              </footer>
            </div>
        </div>


    </div>

</template>

<script>

</script>