var gulp = require('gulp');
var sourcemaps = require('gulp-sourcemaps');
var bower = require('bower-files')();
var concat = require('gulp-concat');
var less = require('gulp-less');
var uglify = require('gulp-uglify');
var nodemon = require('gulp-nodemon');
var browserSync = require('browser-sync');
var reload = browserSync.reload;

var paths = {
  'templates': ['./indexy/templates/**/*.html'],
  'styles': ['./indexy/static/styles/**/*.less']
};

gulp.task('less', function() {
  return gulp.src(paths.styles)
    .pipe(sourcemaps.init())
    .pipe(less())
    .pipe(concat('style.css'))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('./indexy/public/styles/'))
    .pipe(reload({stream: true}))
});

gulp.task('bowerdeps', function() {
  return gulp.src(bower.ext('js').files)
    .pipe(sourcemaps.init())
    .pipe(concat('libs.min.js'))
    .pipe(uglify())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('./indexy/public/scripts/'))
});


gulp.task('watch', ['less'], function() {

  //nodemon({
  //  exec: 'python run.py',
  //  watch: ['**/*.py']
  //})

  browserSync({
    proxy: '127.0.0.1:5002',
    files: ['public/**/*.{js,css}']
  });

  gulp.watch(paths.styles, ['less']);
  gulp.watch(paths.templates).on('change', browserSync.reload)
});

gulp.task('default', ['less', 'bowerdeps']);
