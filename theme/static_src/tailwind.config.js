/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    safelist: [
        { pattern: /^bg-/ }, // السماح بجميع الألوان الخلفية
        { pattern: /^text-/ }, // السماح بجميع ألوان النصوص
        { pattern: /^border-/ } // السماح بجميع ألوان الحدود
      ],
    theme: {
        extend: {
            colors: {
              primary: "#1578D8",
              primary_bg: "#F0F6FF",
            },
            keyframes: {
              fadeInDown: {
                "0%": { opacity: "0", transform: "translateY(-50px)" },
                "100%": { opacity: "1", transform: "translateY(0)" },
              },
            },
            animation: {
              fadeInDown: "fadeInDown 1s ease-out forwards",
            },
          },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
