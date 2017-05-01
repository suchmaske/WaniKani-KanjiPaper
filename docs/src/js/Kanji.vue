<template>

    <div class="columns is-multiline">


            <div class="column is-one-quarter" v-for="level in 60">
                <div class="card">
                  <div class="card-content">
                    <p class="title">
                      Level {{ level }}
                    </p>
                    <p class="subtitle">
                      Kanji
                    </p>
                  </div>
                  <footer class="card-footer">
                    <p class="card-footer-item">
                      <a :href=" level | levelUrl">
                          Download
                      </a>
                    </p>
                  </footer>
                </div>
            </div>

        </div>


</template>

<script type="text/babel">

    export default {

        filters : {

            levelUrl(level) {

                return "./dist/pdf/WK-Kanji-" + level + ".pdf"

            }

        }

    }

</script>