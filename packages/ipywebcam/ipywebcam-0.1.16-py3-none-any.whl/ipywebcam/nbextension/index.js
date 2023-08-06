define(["@jupyter-widgets/base"], (__WEBPACK_EXTERNAL_MODULE__jupyter_widgets_base__) => { return /******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./node_modules/css-loader/dist/cjs.js!./css/video.css":
/*!*************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/video.css ***!
  \*************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, "/* ==========================================================================\n   #Custom HTML5 Video Player\n   ========================================================================== */\n\n:root {\n  --youtube-red: #FE0900;\n}\n\n.ipywebcam.video-container {\n  width: 800px;\n  border-radius: 4px;\n  margin: 0 auto;\n  position: relative;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n}\n\n.ipywebcam.video-container .video {\n  width: 100%;\n  height: 100%;\n  border-radius: 4px;\n}\n\n.ipywebcam.video-container .video-controls {\n  right: 0;\n  left: 0;\n  padding: 10px;\n  position: absolute;\n  bottom: 0;\n  transition: all 0.2s ease;\n  background-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.5));\n}\n\n.ipywebcam.video-container .video-controls.hide {\n  opacity: 0;\n  pointer-events: none;\n}\n\n.ipywebcam.video-container .video-progress {\n  position: relative;\n  height: 8.4px;\n  margin-bottom: 10px;\n}\n\n.ipywebcam.video-container progress {\n  -webkit-appearance: none;\n  -moz-appearance: none;\n  appearance: none;\n  border-radius: 2px;\n  width: 100%;\n  height: 8.4px;\n  pointer-events: none;\n  position: absolute;\n  top: 0;\n}\n\n.ipywebcam.video-container progress::-webkit-progress-bar {\n  background-color: #474545;\n  border-radius: 2px;\n}\n\n.ipywebcam.video-container progress::-webkit-progress-value {\n  background: var(--youtube-red);\n  border-radius: 2px;\n}\n\n.ipywebcam.video-container progress::-moz-progress-bar {\n  border: 1px solid var(--youtube-red);\n  background: var(--youtube-red);\n}\n\n.ipywebcam.video-container .seek {\n  position: absolute;\n  top: 0;\n  width: 100%;\n  cursor: pointer;\n  margin: 0;\n}\n\n.ipywebcam.video-container .seek:hover+.seek-tooltip {\n  display: block;\n}\n\n.ipywebcam.video-container .seek-tooltip {\n  display: none;\n  position: absolute;\n  top: -50px;\n  margin-left: -20px;\n  font-size: 12px;\n  padding: 3px;\n  content: attr(data-title);\n  font-weight: bold;\n  color: #fff;\n  background-color: rgba(0, 0, 0, 0.6);\n}\n\n.ipywebcam.video-container .bottom-controls {\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n}\n\n.ipywebcam.video-container .left-controls {\n  display: flex;\n  align-items: center;\n  color: #fff;\n}\n\n.ipywebcam.video-container .volume-controls {\n  display: flex;\n  align-items: center;\n  margin-right: 10px;\n}\n\n.ipywebcam.video-container .volume-controls input {\n  width: 100px;\n  opacity: 1;\n  transition: all 0.4s ease;\n}\n\n.ipywebcam.video-container .volume-controls:hover input, .volume-controls input:focus {\n  width: 100px;\n  opacity: 1;\n}\n\n.ipywebcam.video-container button {\n  cursor: pointer;\n  position: relative;\n  margin-right: 7px;\n  font-size: 12px;\n  padding: 3px;\n  border: none;\n  outline: none;\n  background-color: transparent;\n}\n\n.ipywebcam.video-container button * {\n  pointer-events: none;\n}\n\n.ipywebcam.video-container button:not(.no-tooltip)::before {\n  content: attr(data-title);\n  position: absolute;\n  display: none;\n  right: 0;\n  top: -50px;\n  background-color: rgba(0, 0, 0, 0.6);\n  color: #fff;\n  font-weight: bold;\n  padding: 4px 6px;\n  word-break: keep-all;\n  white-space: pre;\n}\n\n.ipywebcam.video-container button:not(.no-tooltip):hover::before {\n  display: inline-block;\n}\n\n.ipywebcam.video-container .fullscreen-button {\n  margin-right: 0;\n}\n\n.ipywebcam.video-container .index-selector {\n  color: #fff;\n  min-width: 26px;\n  height: 26px;\n}\n\n.ipywebcam.video-container .selector-panel {\n  position: absolute;\n  border: none;\n  border-radius: 4px;\n  background: rgba(21, 21, 21, .9);\n  padding: 6px 12px;\n}\n\n.ipywebcam.video-container .selector-options {\n  display: flex;\n  flex-wrap: wrap;\n}\n\n.ipywebcam.video-container .selector-pager {\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n}\n\n.ipywebcam.video-container .selector-pager svg {\n  width: 20px;\n  height: 20px;\n}\n\n.ipywebcam.video-container .selector-pager svg.disabled {\n  fill: #aaa;\n  stroke: #aaa;\n}\n\n.ipywebcam.video-container button.selector-option {\n  color: #fff;\n  min-width: 26px;\n  height: 26px;\n  margin: 3px;\n  pointer-events: auto;\n}\n\n.ipywebcam.video-container button.selector-option:hover {\n  background: rgba(120, 120, 120, 0.9);\n}\n\n.ipywebcam.video-container .pip-button svg {\n  width: 26px;\n  height: 26px;\n}\n\n.ipywebcam.video-container .playback-animation {\n  pointer-events: none;\n  position: absolute;\n  top: 50%;\n  left: 50%;\n  margin-left: -40px;\n  margin-top: -40px;\n  width: 80px;\n  height: 80px;\n  border-radius: 80px;\n  background-color: rgba(0, 0, 0, 0.6);\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  opacity: 0;\n}\n\n.ipywebcam.video-container input[type=range] {\n  -webkit-appearance: none;\n  -moz-appearance: none;\n  height: 8.4px;\n  background: transparent;\n  cursor: pointer;\n}\n\n.ipywebcam.video-container input[type=range]:focus {\n  outline: none;\n}\n\n.ipywebcam.video-container input[type=range]::-webkit-slider-runnable-track {\n  width: 100%;\n  cursor: pointer;\n  border-radius: 1.3px;\n  -webkit-appearance: none;\n  transition: all 0.4s ease;\n}\n\n.ipywebcam.video-container input[type=range]::-webkit-slider-thumb {\n  height: 16px;\n  width: 16px;\n  border-radius: 16px;\n  background: var(--youtube-red);\n  cursor: pointer;\n  -webkit-appearance: none;\n  margin-left: -1px;\n}\n\n.ipywebcam.video-container input[type=range]:focus::-webkit-slider-runnable-track {\n  background: transparent;\n}\n\n.ipywebcam.video-container input[type=range].volume {\n  height: 5px;\n  background-color: #fff;\n}\n\n.ipywebcam.video-container input[type=range].volume::-webkit-slider-runnable-track {\n  background-color: transparent;\n}\n\n.ipywebcam.video-container input[type=range].volume::-webkit-slider-thumb {\n  margin-left: 0;\n  height: 14px;\n  width: 14px;\n  background: #fff;\n}\n\n.ipywebcam.video-container input[type=range]::-moz-range-track {\n  width: 100%;\n  height: 8.4px;\n  cursor: pointer;\n  border: 1px solid transparent;\n  background: transparent;\n  border-radius: 1.3px;\n}\n\n.ipywebcam.video-container input[type=range]::-moz-range-thumb {\n  height: 14px;\n  width: 14px;\n  border-radius: 50px;\n  border: 1px solid var(--youtube-red);\n  background: var(--youtube-red);\n  cursor: pointer;\n  margin-top: 5px;\n}\n\n.ipywebcam.video-container input[type=range]:focus::-moz-range-track {\n  outline: none;\n}\n\n.ipywebcam.video-container input[type=range].volume::-moz-range-thumb {\n  border: 1px solid #fff;\n  background: #fff;\n}\n\n.ipywebcam.video-container .hidden {\n  display: none;\n}\n\n.ipywebcam.video-container svg {\n  width: 28px;\n  height: 28px;\n  fill: #fff;\n  stroke: #fff;\n  cursor: pointer;\n  vertical-align: middle;\n}", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".custom-widget {\n  background-color: lightseagreen;\n  padding: 0px 2px;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {

"use strict";


/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
// eslint-disable-next-line func-names
module.exports = function (useSourceMap) {
  var list = []; // return the list of modules as css string

  list.toString = function toString() {
    return this.map(function (item) {
      var content = cssWithMappingToString(item, useSourceMap);

      if (item[2]) {
        return "@media ".concat(item[2], " {").concat(content, "}");
      }

      return content;
    }).join('');
  }; // import a list of modules into the list
  // eslint-disable-next-line func-names


  list.i = function (modules, mediaQuery, dedupe) {
    if (typeof modules === 'string') {
      // eslint-disable-next-line no-param-reassign
      modules = [[null, modules, '']];
    }

    var alreadyImportedModules = {};

    if (dedupe) {
      for (var i = 0; i < this.length; i++) {
        // eslint-disable-next-line prefer-destructuring
        var id = this[i][0];

        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }

    for (var _i = 0; _i < modules.length; _i++) {
      var item = [].concat(modules[_i]);

      if (dedupe && alreadyImportedModules[item[0]]) {
        // eslint-disable-next-line no-continue
        continue;
      }

      if (mediaQuery) {
        if (!item[2]) {
          item[2] = mediaQuery;
        } else {
          item[2] = "".concat(mediaQuery, " and ").concat(item[2]);
        }
      }

      list.push(item);
    }
  };

  return list;
};

function cssWithMappingToString(item, useSourceMap) {
  var content = item[1] || ''; // eslint-disable-next-line prefer-destructuring

  var cssMapping = item[3];

  if (!cssMapping) {
    return content;
  }

  if (useSourceMap && typeof btoa === 'function') {
    var sourceMapping = toComment(cssMapping);
    var sourceURLs = cssMapping.sources.map(function (source) {
      return "/*# sourceURL=".concat(cssMapping.sourceRoot || '').concat(source, " */");
    });
    return [content].concat(sourceURLs).concat([sourceMapping]).join('\n');
  }

  return [content].join('\n');
} // Adapted from convert-source-map (MIT)


function toComment(sourceMap) {
  // eslint-disable-next-line no-undef
  var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap))));
  var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
  return "/*# ".concat(data, " */");
}

/***/ }),

/***/ "./css/video.css":
/*!***********************!*\
  !*** ./css/video.css ***!
  \***********************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./video.css */ "./node_modules/css-loader/dist/cjs.js!./css/video.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var isOldIE = function isOldIE() {
  var memo;
  return function memorize() {
    if (typeof memo === 'undefined') {
      // Test for IE <= 9 as proposed by Browserhacks
      // @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
      // Tests for existence of standard globals is to allow style-loader
      // to operate correctly into non-standard environments
      // @see https://github.com/webpack-contrib/style-loader/issues/177
      memo = Boolean(window && document && document.all && !window.atob);
    }

    return memo;
  };
}();

var getTarget = function getTarget() {
  var memo = {};
  return function memorize(target) {
    if (typeof memo[target] === 'undefined') {
      var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself

      if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
        try {
          // This will throw an exception if access to iframe is blocked
          // due to cross-origin restrictions
          styleTarget = styleTarget.contentDocument.head;
        } catch (e) {
          // istanbul ignore next
          styleTarget = null;
        }
      }

      memo[target] = styleTarget;
    }

    return memo[target];
  };
}();

var stylesInDom = [];

function getIndexByIdentifier(identifier) {
  var result = -1;

  for (var i = 0; i < stylesInDom.length; i++) {
    if (stylesInDom[i].identifier === identifier) {
      result = i;
      break;
    }
  }

  return result;
}

function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];

  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var index = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3]
    };

    if (index !== -1) {
      stylesInDom[index].references++;
      stylesInDom[index].updater(obj);
    } else {
      stylesInDom.push({
        identifier: identifier,
        updater: addStyle(obj, options),
        references: 1
      });
    }

    identifiers.push(identifier);
  }

  return identifiers;
}

function insertStyleElement(options) {
  var style = document.createElement('style');
  var attributes = options.attributes || {};

  if (typeof attributes.nonce === 'undefined') {
    var nonce =  true ? __webpack_require__.nc : 0;

    if (nonce) {
      attributes.nonce = nonce;
    }
  }

  Object.keys(attributes).forEach(function (key) {
    style.setAttribute(key, attributes[key]);
  });

  if (typeof options.insert === 'function') {
    options.insert(style);
  } else {
    var target = getTarget(options.insert || 'head');

    if (!target) {
      throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
    }

    target.appendChild(style);
  }

  return style;
}

function removeStyleElement(style) {
  // istanbul ignore if
  if (style.parentNode === null) {
    return false;
  }

  style.parentNode.removeChild(style);
}
/* istanbul ignore next  */


var replaceText = function replaceText() {
  var textStore = [];
  return function replace(index, replacement) {
    textStore[index] = replacement;
    return textStore.filter(Boolean).join('\n');
  };
}();

function applyToSingletonTag(style, index, remove, obj) {
  var css = remove ? '' : obj.media ? "@media ".concat(obj.media, " {").concat(obj.css, "}") : obj.css; // For old IE

  /* istanbul ignore if  */

  if (style.styleSheet) {
    style.styleSheet.cssText = replaceText(index, css);
  } else {
    var cssNode = document.createTextNode(css);
    var childNodes = style.childNodes;

    if (childNodes[index]) {
      style.removeChild(childNodes[index]);
    }

    if (childNodes.length) {
      style.insertBefore(cssNode, childNodes[index]);
    } else {
      style.appendChild(cssNode);
    }
  }
}

function applyToTag(style, options, obj) {
  var css = obj.css;
  var media = obj.media;
  var sourceMap = obj.sourceMap;

  if (media) {
    style.setAttribute('media', media);
  } else {
    style.removeAttribute('media');
  }

  if (sourceMap && typeof btoa !== 'undefined') {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  } // For old IE

  /* istanbul ignore if  */


  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
    while (style.firstChild) {
      style.removeChild(style.firstChild);
    }

    style.appendChild(document.createTextNode(css));
  }
}

var singleton = null;
var singletonCounter = 0;

function addStyle(obj, options) {
  var style;
  var update;
  var remove;

  if (options.singleton) {
    var styleIndex = singletonCounter++;
    style = singleton || (singleton = insertStyleElement(options));
    update = applyToSingletonTag.bind(null, style, styleIndex, false);
    remove = applyToSingletonTag.bind(null, style, styleIndex, true);
  } else {
    style = insertStyleElement(options);
    update = applyToTag.bind(null, style, options);

    remove = function remove() {
      removeStyleElement(style);
    };
  }

  update(obj);
  return function updateStyle(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap) {
        return;
      }

      update(obj = newObj);
    } else {
      remove();
    }
  };
}

module.exports = function (list, options) {
  options = options || {}; // Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
  // tags it will allow on a page

  if (!options.singleton && typeof options.singleton !== 'boolean') {
    options.singleton = isOldIE();
  }

  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];

    if (Object.prototype.toString.call(newList) !== '[object Array]') {
      return;
    }

    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDom[index].references--;
    }

    var newLastIdentifiers = modulesToDom(newList, options);

    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];

      var _index = getIndexByIdentifier(_identifier);

      if (stylesInDom[_index].references === 0) {
        stylesInDom[_index].updater();

        stylesInDom.splice(_index, 1);
      }
    }

    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./src/common.ts":
/*!***********************!*\
  !*** ./src/common.ts ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.BaseModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./src/version.ts");
class BaseModel extends base_1.DOMWidgetModel {
    constructor(...args) {
        super(...args);
        this.messageHandlers = {};
        this.addMessageHandler = (cmd, handler) => {
            this.messageHandlers[cmd] = handler;
        };
        this.send_cmd = this.send_cmd.bind(this);
        this.on('msg:custom', (msg, buffers) => {
            const { id, cmd } = msg;
            if (id !== this.message_id) {
                return;
            }
            Object.keys(this.messageHandlers).forEach((key) => {
                if (key === cmd) {
                    const handler = this.messageHandlers[key];
                    if (handler) {
                        handler(msg, buffers);
                    }
                }
            });
        });
    }
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _view_module: version_1.MODULE_NAME, _model_module: version_1.MODULE_NAME, _view_module_version: version_1.MODULE_VERSION, _model_module_version: version_1.MODULE_VERSION });
    }
    get message_id() {
        return this.model_id;
    }
    send_cmd(cmd, args, wait = true) {
        return __awaiter(this, void 0, void 0, function* () {
            const id = this.message_id;
            if (wait) {
                return new Promise((resolve) => {
                    // eslint-disable-next-line @typescript-eslint/no-this-alias
                    const self = this;
                    this.send({ cmd, id, args }, {});
                    function callback({ ans, id: t_id, res, }, buffers) {
                        if (ans === cmd && t_id === id) {
                            resolve({ content: res, buffers });
                            self.off('msg:custom', callback);
                        }
                    }
                    this.on('msg:custom', callback);
                });
            }
            else {
                this.send({ cmd, id, args }, {});
            }
        });
    }
}
exports.BaseModel = BaseModel;


/***/ }),

/***/ "./src/extension.ts":
/*!**************************!*\
  !*** ./src/extension.ts ***!
  \**************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
// Entry point for the notebook bundle containing custom model definitions.
//
// Setup notebook base URL
//
// Some static assets may be required by the custom widget javascript. The base
// url for the notebook is not known at build time and is therefore computed
// dynamically.
// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
window.__webpack_public_path__ =
    document.querySelector('body').getAttribute('data-base-url') +
        'nbextensions/ipywebcam';
__exportStar(__webpack_require__(/*! ./index */ "./src/index.ts"), exports);


/***/ }),

/***/ "./src/index.ts":
/*!**********************!*\
  !*** ./src/index.ts ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Xiaojing Chen
// Distributed under the terms of the Modified BSD License.
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
__exportStar(__webpack_require__(/*! ./version */ "./src/version.ts"), exports);
__exportStar(__webpack_require__(/*! ./webcam */ "./src/webcam.ts"), exports);
__exportStar(__webpack_require__(/*! ./recorder */ "./src/recorder.ts"), exports);


/***/ }),

/***/ "./src/recorder.ts":
/*!*************************!*\
  !*** ./src/recorder.ts ***!
  \*************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.RecorderPlayerView = exports.RecorderPlayerModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "@jupyter-widgets/base");
const lru_cache_1 = __importDefault(__webpack_require__(/*! lru-cache */ "./node_modules/lru-cache/index.js"));
const common_1 = __webpack_require__(/*! ./common */ "./src/common.ts");
const video_1 = __webpack_require__(/*! ./video */ "./src/video.ts");
class RecorderPlayerModel extends common_1.BaseModel {
    constructor(...args) {
        super(...args);
        this.cache = new lru_cache_1.default({
            max: 6,
        });
        this.fetchStates = {};
        this.refresh_callbacks = [];
        this.addRefereshCallback = (callback) => {
            this.refresh_callbacks.push(callback);
        };
        this.removeRefreshCallback = (callback) => {
            const index = this.refresh_callbacks.indexOf(callback);
            if (index >= 0) {
                this.refresh_callbacks.splice(index, 1);
            }
        };
        this.triggerRefresh = (index, channel) => {
            this.refresh_callbacks.forEach((cb) => {
                cb(index, channel);
            });
        };
        this.fetchMeta = () => __awaiter(this, void 0, void 0, function* () {
            if (this.meta) {
                return this.meta;
            }
            const { content } = yield this.send_cmd('fetch_meta', {});
            this.meta = content;
            return this.meta;
        });
        this.fetchData = (index, channel) => __awaiter(this, void 0, void 0, function* () {
            const key = channel ? `${index}-${channel}` : `${index}`;
            const cached = this.cache.get(key);
            if (cached) {
                return cached;
            }
            let fetchState = this.fetchStates[key];
            if (!fetchState) {
                fetchState = {
                    callbacks: [],
                };
                this.fetchStates[key] = fetchState;
                const { content, buffers } = yield this.send_cmd('fetch_data', {
                    index,
                    channel,
                });
                const { format = this.get('format') } = content;
                const blob = new Blob(buffers, { type: format });
                this.cache.set(key, blob);
                fetchState.callbacks.forEach((callback) => callback(blob));
                delete this.fetchStates[key];
                return blob;
            }
            else {
                let theResolve = undefined;
                fetchState.callbacks.push((blob) => {
                    if (theResolve) {
                        theResolve(blob);
                    }
                    else {
                        throw new Error('This is impossible! No resovle method found. It seems that the promise is not invoked yet.');
                    }
                });
                return new Promise((resolve) => {
                    theResolve = resolve;
                });
            }
        });
        this.addMessageHandler('channel_stale', (cmdMsg) => {
            const { args = {} } = cmdMsg;
            const { channel } = args;
            if (channel) {
                for (const key of this.cache.keys()) {
                    if (key.endsWith(`-${channel}`)) {
                        this.cache.delete(key);
                    }
                }
            }
            else {
                this.cache.clear();
            }
            this.triggerRefresh(undefined, channel);
        });
    }
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: RecorderPlayerModel.model_name, _view_name: RecorderPlayerModel.view_name, format: 'mp4', width: '', height: '', autoplay: true, loop: false, controls: true });
    }
}
exports.RecorderPlayerModel = RecorderPlayerModel;
RecorderPlayerModel.model_name = 'RecorderPlayerModel';
RecorderPlayerModel.view_name = 'RecorderPlayerView'; // Set to null if no view
class RecorderPlayerView extends base_1.DOMWidgetView {
    constructor(...args) {
        super(...args);
        this.index = -1;
        this.channel = '';
        this.initVideo = () => __awaiter(this, void 0, void 0, function* () {
            if (!this.video) {
                this.video = new video_1.Video();
                this.video.addSelectHandler((i) => {
                    this.load(i, undefined);
                });
                this.el.appendChild(this.video.container);
                const { record_count = 0, chanels = [] } = yield this.model.fetchMeta();
                if (record_count > 0) {
                    yield this.load(0, chanels.length > 0 ? chanels[0] : '');
                }
                else {
                    this.video.updateIndexerSize(0);
                }
                this.update();
            }
        });
        this.load = (index, channel, force = false) => __awaiter(this, void 0, void 0, function* () {
            if (this.video) {
                if (typeof index === 'undefined') {
                    index = this.index;
                }
                if (typeof channel === 'undefined') {
                    channel = this.channel;
                }
                if (this.index === index && this.channel === channel && !force) {
                    return;
                }
                const { record_count = 0 } = yield this.model.fetchMeta();
                try {
                    this.video.updateIndexerSize(record_count);
                    const blob = yield this.model.fetchData(index, channel);
                    this.video.updateData(blob);
                    this.index = index;
                    this.channel = channel;
                    this.video.updateIndexerIndex(this.index);
                }
                catch (e) {
                    console.error(e);
                }
            }
        });
        this.updateWidth = () => {
            var _a, _b;
            const width = this.model.get('width');
            if (width !== undefined && width.length > 0) {
                (_a = this.video) === null || _a === void 0 ? void 0 : _a.video.setAttribute('width', width);
            }
            else {
                (_b = this.video) === null || _b === void 0 ? void 0 : _b.video.removeAttribute('width');
            }
        };
        this.updateHeight = () => {
            var _a, _b;
            const height = this.model.get('height');
            if (height !== undefined && height.length > 0) {
                (_a = this.video) === null || _a === void 0 ? void 0 : _a.video.setAttribute('height', height);
            }
            else {
                (_b = this.video) === null || _b === void 0 ? void 0 : _b.video.removeAttribute('height');
            }
        };
        this.updateOtherVideoAttributes = () => {
            var _a, _b, _c;
            (_a = this.video) === null || _a === void 0 ? void 0 : _a.video.setAttribute('loop', this.model.get('loop'));
            (_b = this.video) === null || _b === void 0 ? void 0 : _b.video.setAttribute('autoplay', this.model.get('autoplay'));
            (_c = this.video) === null || _c === void 0 ? void 0 : _c.enableControls(this.model.get('controls'));
        };
        this.model.addRefereshCallback((i, c) => {
            if (this.index === i &&
                ((!this.channel && !c) || (this.channel && c && this.channel === c))) {
                this.load(undefined, undefined, true);
            }
        });
    }
    render() {
        super.render();
        this.initVideo();
    }
    update() {
        this.updateWidth();
        this.updateHeight();
        this.updateOtherVideoAttributes();
        return super.update();
    }
    remove() {
        var _a;
        (_a = this.video) === null || _a === void 0 ? void 0 : _a.destroy();
        this.video = undefined;
    }
}
exports.RecorderPlayerView = RecorderPlayerView;


/***/ }),

/***/ "./src/utils.ts":
/*!**********************!*\
  !*** ./src/utils.ts ***!
  \**********************/
/***/ ((__unused_webpack_module, exports) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.isMac = exports.arrayFind = exports.arrayInclude = void 0;
function arrayInclude(arr, target) {
    return !!~arr.indexOf(target);
}
exports.arrayInclude = arrayInclude;
function arrayFind(arr, cond) {
    for (let i = 0; i < arr.length; ++i) {
        const e = arr[i];
        if (cond(e, i)) {
            return e;
        }
    }
    return undefined;
}
exports.arrayFind = arrayFind;
function isMac() {
    return window.navigator.userAgent.indexOf('Mac') !== -1;
}
exports.isMac = isMac;


/***/ }),

/***/ "./src/version.ts":
/*!************************!*\
  !*** ./src/version.ts ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Xiaojing Chen
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;


/***/ }),

/***/ "./src/video.ts":
/*!**********************!*\
  !*** ./src/video.ts ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/* eslint-disable @typescript-eslint/no-non-null-assertion */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Video = exports.createVideoContainer = exports.createVideoProgress = exports.createPlaybackAnimation = exports.createSelectiveUses = exports.makeId = void 0;
__webpack_require__(/*! ../css/video.css */ "./css/video.css");
const svgNS = 'http://www.w3.org/2000/svg';
const prefix = 'ipywebcam-video-';
function makeId(id) {
    return `${prefix}${id}`;
}
exports.makeId = makeId;
function createSymbol(id, pathD, viewBox = '0 0 24 24') {
    const symbol = document.createElementNS(svgNS, 'symbol');
    symbol.id = makeId(id);
    symbol.setAttribute('viewBox', viewBox);
    const path = document.createElementNS(svgNS, 'path');
    path.setAttribute('d', pathD);
    symbol.appendChild(path);
    return symbol;
}
function createControlsSvg() {
    const svg = document.createElementNS(svgNS, 'svg');
    svg.id = makeId('icons');
    svg.setAttribute('style', 'display: none');
    const defs = document.createElementNS(svgNS, 'defs');
    svg.appendChild(defs);
    defs.appendChild(createSymbol('pause', 'M14.016 5.016h3.984v13.969h-3.984v-13.969zM6 18.984v-13.969h3.984v13.969h-3.984z'));
    defs.appendChild(createSymbol('play-icon', 'M8.016 5.016l10.969 6.984-10.969 6.984v-13.969z'));
    defs.appendChild(createSymbol('volume-high', 'M14.016 3.234q3.047 0.656 5.016 3.117t1.969 5.648-1.969 5.648-5.016 3.117v-2.063q2.203-0.656 3.586-2.484t1.383-4.219-1.383-4.219-3.586-2.484v-2.063zM16.5 12q0 2.813-2.484 4.031v-8.063q1.031 0.516 1.758 1.688t0.727 2.344zM3 9h3.984l5.016-5.016v16.031l-5.016-5.016h-3.984v-6z'));
    defs.appendChild(createSymbol('volume-low', 'M5.016 9h3.984l5.016-5.016v16.031l-5.016-5.016h-3.984v-6zM18.516 12q0 2.766-2.531 4.031v-8.063q1.031 0.516 1.781 1.711t0.75 2.32z'));
    defs.appendChild(createSymbol('volume-mute', 'M12 3.984v4.219l-2.109-2.109zM4.266 3l16.734 16.734-1.266 1.266-2.063-2.063q-1.547 1.313-3.656 1.828v-2.063q1.172-0.328 2.25-1.172l-4.266-4.266v6.75l-5.016-5.016h-3.984v-6h4.734l-4.734-4.734zM18.984 12q0-2.391-1.383-4.219t-3.586-2.484v-2.063q3.047 0.656 5.016 3.117t1.969 5.648q0 2.203-1.031 4.172l-1.5-1.547q0.516-1.266 0.516-2.625zM16.5 12q0 0.422-0.047 0.609l-2.438-2.438v-2.203q1.031 0.516 1.758 1.688t0.727 2.344z'));
    defs.appendChild(createSymbol('fullscreen', 'M14.016 5.016h4.969v4.969h-1.969v-3h-3v-1.969zM17.016 17.016v-3h1.969v4.969h-4.969v-1.969h3zM5.016 9.984v-4.969h4.969v1.969h-3v3h-1.969zM6.984 14.016v3h3v1.969h-4.969v-4.969h1.969z'));
    defs.appendChild(createSymbol('fullscreen-exit', 'M15.984 8.016h3v1.969h-4.969v-4.969h1.969v3zM14.016 18.984v-4.969h4.969v1.969h-3v3h-1.969zM8.016 8.016v-3h1.969v4.969h-4.969v-1.969h3zM5.016 15.984v-1.969h4.969v4.969h-1.969v-3h-3z'));
    defs.appendChild(createSymbol('pip', 'M21 19.031v-14.063h-18v14.063h18zM23.016 18.984q0 0.797-0.609 1.406t-1.406 0.609h-18q-0.797 0-1.406-0.609t-0.609-1.406v-14.016q0-0.797 0.609-1.383t1.406-0.586h18q0.797 0 1.406 0.586t0.609 1.383v14.016zM18.984 11.016v6h-7.969v-6h7.969z'));
    defs.appendChild(createSymbol('left-arrow', 'M15.293 3.293 6.586 12l8.707 8.707 1.414-1.414L9.414 12l7.293-7.293-1.414-1.414z'));
    defs.appendChild(createSymbol('right-arrow', 'M7.293 4.707 14.586 12l-7.293 7.293 1.414 1.414L17.414 12 8.707 3.293 7.293 4.707z'));
    return svg;
}
function createSelectiveUses(active, ...ids) {
    const svg = document.createElementNS(svgNS, 'svg');
    ids.forEach((id) => {
        const use = document.createElementNS(svgNS, 'use');
        use.classList.add(`use-${id}`);
        use.setAttribute('href', `#${makeId(id)}`);
        if (id !== active) {
            use.classList.add('hidden');
        }
        svg.appendChild(use);
    });
    return svg;
}
exports.createSelectiveUses = createSelectiveUses;
function createPlaybackAnimation() {
    const div = document.createElement('div');
    div.id = makeId('playback-animation');
    div.className = 'playback-animation';
    const svg = createSelectiveUses('pause', 'play-icon', 'pause');
    svg.classList.add('playback-icons');
    div.appendChild(svg);
    return div;
}
exports.createPlaybackAnimation = createPlaybackAnimation;
function createVideoProgress() {
    const container = document.createElement('div');
    container.classList.add('video-progress');
    const progress = document.createElement('progress');
    progress.id = makeId('progress-bar');
    progress.classList.add('progress-bar');
    progress.value = progress.max = 0;
    const input = document.createElement('input');
    input.id = makeId('seek');
    input.classList.add('seek');
    input.type = 'range';
    input.value = '0';
    input.min = '0';
    input.step = '1';
    const tooltip = document.createElement('div');
    tooltip.id = makeId('seek-tooltip');
    tooltip.classList.add('seek-tooltip');
    tooltip.innerText = '00:00';
    container.appendChild(progress);
    container.appendChild(input);
    container.appendChild(tooltip);
    return container;
}
exports.createVideoProgress = createVideoProgress;
function createPlaybackButton(options) {
    const button = document.createElement('button');
    button.id = makeId('play');
    button.classList.add('play');
    button.setAttribute('data-title', `Play (${descShortcut(options.shortcuts.play)})`);
    const svg = createSelectiveUses('play-icon', 'play-icon', 'pause');
    svg.classList.add('playback-icons');
    button.appendChild(svg);
    return button;
}
function createVolumeButton(options) {
    const button = document.createElement('button');
    button.id = makeId('volume-button');
    button.classList.add('volume-button');
    button.setAttribute('data-title', `Mute (${descShortcut(options.shortcuts.mute)})`);
    const svg = createSelectiveUses('volume-high', 'volume-mute', 'volume-low', 'volume-high');
    svg.classList.add('volume-icons');
    button.appendChild(svg);
    return button;
}
function createVolumeInput() {
    const input = document.createElement('input');
    input.id = makeId('volume');
    input.classList.add('volume');
    input.value = '1';
    input.type = 'range';
    input.min = '0';
    input.max = '1';
    input.step = '0.01';
    input.setAttribute('data-mute', '0.5');
    return input;
}
function createVolumeControls(options) {
    const container = document.createElement('div');
    container.classList.add('volume-controls');
    const button = createVolumeButton(options);
    container.appendChild(button);
    const input = createVolumeInput();
    container.appendChild(input);
    return container;
}
function createTime() {
    const container = document.createElement('div');
    container.classList.add('time');
    const elapsed = document.createElement('time');
    elapsed.id = makeId('time-elapsed');
    elapsed.classList.add('time-elapsed');
    elapsed.innerText = '00:00';
    container.appendChild(elapsed);
    const span = document.createElement('span');
    span.innerText = ' / ';
    container.appendChild(span);
    const duration = document.createElement('time');
    duration.id = makeId('duration');
    duration.classList.add('duration');
    duration.innerText = '00:00';
    container.appendChild(duration);
    return container;
}
function createLeftControls(options) {
    const container = document.createElement('div');
    container.classList.add('left-controls');
    const playbackButton = createPlaybackButton(options);
    container.appendChild(playbackButton);
    const volumeControls = createVolumeControls(options);
    container.appendChild(volumeControls);
    const time = createTime();
    container.appendChild(time);
    return container;
}
function createIndexSelector() {
    const container = document.createElement('button');
    container.id = makeId('index-selector');
    container.classList.add('index-selector');
    container.setAttribute('data-title', 'Index Select');
    return container;
}
function createPipButton(options) {
    const button = document.createElement('button');
    button.id = makeId('pip-button');
    button.classList.add('pip-button');
    if (!isPipEnabled()) {
        button.classList.add('hidden');
    }
    button.setAttribute('data-title', `PIP (${descShortcut(options.shortcuts.pip)})`);
    const svg = createSelectiveUses('pip', 'pip');
    button.appendChild(svg);
    return button;
}
function createFullscreenButton(options) {
    const button = document.createElement('button');
    button.id = makeId('fullscreen-button');
    button.classList.add('fullscreen-button');
    button.setAttribute('data-title', `Full screen (${descShortcut(options.shortcuts.fullscreen)})`);
    const svg = createSelectiveUses('fullscreen', 'fullscreen', 'fullscreen-exit');
    button.appendChild(svg);
    return button;
}
function createRightControls(options) {
    const container = document.createElement('div');
    container.classList.add('right-controls');
    const indexSelector = createIndexSelector();
    container.appendChild(indexSelector);
    const pipButton = createPipButton(options);
    container.appendChild(pipButton);
    const fullscreenButton = createFullscreenButton(options);
    container.appendChild(fullscreenButton);
    return container;
}
function createBottomControls(options) {
    const container = document.createElement('div');
    container.classList.add('bottom-controls');
    const leftControls = createLeftControls(options);
    container.appendChild(leftControls);
    const rightControls = createRightControls(options);
    container.appendChild(rightControls);
    return container;
}
function createVideoControls(options) {
    const container = document.createElement('div');
    container.classList.add('video-controls');
    container.tabIndex = 0;
    const videoProgress = createVideoProgress();
    container.appendChild(videoProgress);
    const bottomControls = createBottomControls(options);
    container.appendChild(bottomControls);
    return container;
}
const VIDEO_WORKS = !!document.createElement('video').canPlayType;
function createVideoContainer(options) {
    const container = document.createElement('div');
    container.id = makeId('container');
    container.classList.add('ipywebcam');
    container.classList.add('video-container');
    const playbackAnimation = createPlaybackAnimation();
    container.appendChild(playbackAnimation);
    const video = document.createElement('video');
    video.id = makeId('video');
    video.classList.add('video');
    container.appendChild(video);
    const videoControls = createVideoControls(options);
    container.appendChild(videoControls);
    return container;
}
exports.createVideoContainer = createVideoContainer;
function iconShow(svg, id) {
    const uses = svg.getElementsByTagNameNS(svgNS, 'use');
    for (let i = 0; i < uses.length; ++i) {
        const use = uses[i];
        if (use.classList.contains(`use-${id}`)) {
            use.classList.remove('hidden');
        }
        else {
            use.classList.add('hidden');
        }
    }
}
function isPipEnabled() {
    return !!document.pictureInPictureEnabled;
}
class IndexSelectorPannel {
    constructor(size) {
        this.clickHandlers = [];
        this.realClickHandlers = [];
        this.calcLayout = () => {
            this.row = Math.ceil(this.size / 4);
            this.column = Math.min(this.size, 4);
            this.hasPager = this.row > 6;
            this.pageIndex = 0;
            this.pageSize = Math.ceil(this.size / 24);
            this.optionsWidth = this.column * 32 + (this.column - 1) * 6 + 6;
            this.optionsHeight =
                Math.min(this.row, 6) * 32 + (Math.min(this.row, 6) - 1) * 6 + 6;
            const height = this.optionsHeight + 32;
            this.container.style.width = `${this.optionsWidth}px`;
            this.container.style.height = `${height}px`;
            this.container.style.left = `${-this.optionsWidth / 2}px`;
            this.container.style.top = `${-height}px`;
        };
        this.show = () => {
            this.container.classList.remove('hidden');
        };
        this.hidden = () => {
            this.container.classList.add('hidden');
        };
        this.addClickHandler = (handler) => {
            this.clickHandlers.push(handler);
        };
        this.setSelectIndex = (index) => {
            this.container.querySelectorAll('button.selector-option').forEach((e) => {
                e.classList.remove('selected');
            });
            const option = this.container.querySelector(`button.selector-option-${index}`);
            if (option) {
                option.classList.add('selected');
            }
        };
        this.createHandler = (index) => {
            return (evt) => {
                evt.stopPropagation();
                try {
                    (this.clickHandlers || []).forEach((handler) => {
                        handler(index);
                    });
                    this.hidden();
                }
                catch (e) {
                    console.error(e);
                }
            };
        };
        this.updatePage = (pageIndex) => {
            if (pageIndex !== this.pageIndex) {
                this.pageIndex = pageIndex;
                const optNum = this.pageIndex < this.pageSize ? 24 : 24 - (this.size % 24);
                let len = this.options.children.length;
                let idx = 0;
                if (this.realClickHandlers.length > optNum) {
                    this.realClickHandlers.splice(optNum, this.realClickHandlers.length - optNum);
                }
                for (let i = 0; i < len; ++i) {
                    const child = this.options.children.item(i);
                    if (child === null || child === void 0 ? void 0 : child.classList.contains('selector-option')) {
                        const button = child;
                        const dataIdx = idx + (pageIndex - 1) * 24;
                        const newHandler = this.createHandler(dataIdx);
                        if (idx < optNum) {
                            const oldHandler = this.realClickHandlers[idx];
                            button.removeEventListener('click', oldHandler);
                            button.addEventListener('click', newHandler);
                            button.innerText = `${dataIdx}`;
                            ++idx;
                        }
                        else {
                            this.options.removeChild(button);
                            --i;
                            --len;
                        }
                    }
                }
                if (idx < optNum) {
                    for (let i = idx; i < optNum; ++i) {
                        const dataIdx = i + (pageIndex - 1) * 24;
                        const option = document.createElement('button');
                        option.innerText = `${dataIdx}`;
                        option.classList.add('selector-option');
                        option.classList.add('no-tooltip');
                        option.classList.add(`selector-option-${dataIdx}`);
                        option.setAttribute('data-index', `${dataIdx}`);
                        const handler = this.createHandler(dataIdx);
                        this.realClickHandlers.push(handler);
                        option.addEventListener('click', handler);
                        this.options.appendChild(option);
                    }
                }
                if (this.hasPager) {
                    if (this.pager) {
                        if (this.pagerLeft && this.pageIndex <= 1) {
                            this.pagerLeft.classList.add('disabled');
                        }
                        if (this.pagerNumber) {
                            this.pagerNumber.innerText = `${pageIndex} / ${this.pageSize}`;
                        }
                        if (this.pagerRight && this.pageIndex >= this.pageSize) {
                            this.pagerRight.classList.add('disabled');
                        }
                    }
                    else {
                        this.pager = document.createElement('div');
                        this.pager.classList.add('selector-pager');
                        this.pagerLeft = document.createElement('button');
                        this.pagerLeft.classList.add('page-left');
                        this.pagerLeft.classList.add('no-tooltip');
                        this.pagerLeft.appendChild(createSelectiveUses('page-left', 'page-left'));
                        if (this.pageIndex <= 1) {
                            this.pagerLeft.classList.add('disabled');
                        }
                        this.pagerLeft.addEventListener('click', () => {
                            if (this.pageIndex > 1) {
                                this.updatePage(this.pageIndex - 1);
                            }
                        });
                        this.pager.appendChild(this.pagerLeft);
                        this.pagerNumber = document.createElement('div');
                        this.pagerNumber.innerText = `${pageIndex} / ${this.pageSize}`;
                        this.pager.appendChild(this.pagerNumber);
                        this.pagerRight = document.createElement('button');
                        this.pagerRight.classList.add('page-right');
                        this.pagerRight.classList.add('no-tooltip');
                        this.pagerRight.appendChild(createSelectiveUses('page-right', 'page-right'));
                        if (this.pageIndex >= this.pageSize) {
                            this.pagerRight.classList.add('disabled');
                        }
                        this.pagerRight.addEventListener('click', () => {
                            if (this.pageIndex < this.pageSize) {
                                this.updatePage(this.pageIndex + 1);
                            }
                        });
                        this.pager.appendChild(this.pagerRight);
                        this.container.appendChild(this.pager);
                    }
                }
                else {
                    if (this.pager) {
                        this.container.removeChild(this.pager);
                        this.pager = undefined;
                        this.pagerNumber = undefined;
                    }
                }
            }
        };
        this.updateSize = (size) => {
            if (this.size !== size) {
                this.size = size;
                this.calcLayout();
                this.updatePage(1);
            }
        };
        this.container = document.createElement('div');
        this.container.classList.add('selector-panel');
        this.options = document.createElement('div');
        this.options.classList.add('selector-options');
        this.container.appendChild(this.options);
        this.container.addEventListener('mouseleave', this.hidden);
        this.updateSize(size);
    }
}
function descShortcut(shortcut) {
    const parts = [];
    if (shortcut.ctrl) {
        parts.push('ctrl');
    }
    if (shortcut.alt) {
        parts.push('alt');
    }
    if (shortcut.shift) {
        parts.push('shift');
    }
    parts.push(shortcut.key);
    return parts.join(' + ');
}
const DEFAULT_OPTIONS = {
    shortcuts: {
        play: 'k',
        mute: 'm',
        fullscreen: 'f',
        pip: 'p',
    },
};
function makeShortcut(shortcut) {
    if (typeof shortcut === 'string') {
        return {
            key: shortcut,
            ctrl: false,
            alt: false,
            shift: false,
        };
    }
    else {
        return {
            key: shortcut.key,
            ctrl: shortcut.ctrl || false,
            alt: shortcut.alt || false,
            shift: shortcut.shift || false,
        };
    }
}
function makeOptions(otps) {
    const options = Object.assign({}, DEFAULT_OPTIONS, otps);
    options.shortcuts = Object.assign({}, DEFAULT_OPTIONS.shortcuts, otps.shortcuts);
    options.shortcuts.fullscreen = makeShortcut(options.shortcuts.fullscreen);
    options.shortcuts.mute = makeShortcut(options.shortcuts.mute);
    options.shortcuts.pip = makeShortcut(options.shortcuts.pip);
    options.shortcuts.play = makeShortcut(options.shortcuts.play);
    return options;
}
class Video {
    constructor(opts = {}) {
        this.indexSelectHandlers = [];
        this.destroy = () => {
            document.removeEventListener('keyup', this.keyboardShortcuts);
            const url = this.video.src;
            this.video.src = '';
            if (url) {
                URL.revokeObjectURL(url);
            }
        };
        this.updateIndexerSize = (size) => {
            if (!this.indexSelectorPannel) {
                if (size > 0) {
                    this.indexSelectorPannel = new IndexSelectorPannel(size);
                    this.indexSelectorPannel.hidden();
                    this.indexSelectHandlers.forEach((handler) => {
                        var _a;
                        (_a = this.indexSelectorPannel) === null || _a === void 0 ? void 0 : _a.addClickHandler(handler);
                    });
                    this.indexSelector.parentElement.appendChild(this.indexSelectorPannel.container);
                    this.indexSelector.addEventListener('click', () => {
                        var _a, _b;
                        (_a = this.indexSelectorPannel) === null || _a === void 0 ? void 0 : _a.show();
                        const index = this.indexSelector.getAttribute('data-index');
                        if (index) {
                            (_b = this.indexSelectorPannel) === null || _b === void 0 ? void 0 : _b.setSelectIndex(Number.parseInt(index));
                        }
                    });
                    this.indexSelector.classList.remove('hidden');
                }
                else {
                    this.indexSelector.classList.add('hidden');
                }
            }
            else {
                if (size <= 0) {
                    this.indexSelectorPannel.hidden();
                    this.indexSelector.classList.add('hidden');
                }
                else {
                    this.indexSelectorPannel.updateSize(size);
                    this.indexSelector.classList.remove('hidden');
                }
            }
        };
        this.updateIndexerIndex = (index) => {
            this.indexSelector.innerText = `${index}`;
            this.indexSelector.setAttribute('data-index', `${index}`);
        };
        this.addSelectHandler = (handler) => {
            this.indexSelectHandlers.push(handler);
            if (this.indexSelectorPannel) {
                this.indexSelectorPannel.addClickHandler(handler);
            }
        };
        this.updateData = (blob) => {
            const oldUrl = this.video.src;
            const url = URL.createObjectURL(blob);
            this.video.pause();
            this.video.src = url;
            this.video.load();
            if (oldUrl) {
                URL.revokeObjectURL(this.video.src);
            }
        };
        this.installSvg = () => {
            const id = makeId('icons');
            const svg = document.getElementById(id);
            if (!svg) {
                document.body.appendChild(createControlsSvg());
            }
        };
        this.togglePlay = () => {
            if (this.video.paused || this.video.ended) {
                this.video.play();
            }
            else {
                this.video.pause();
            }
        };
        this.enableControls = (enabled) => {
            if (enabled) {
                if (VIDEO_WORKS) {
                    this.video.controls = false;
                    this.videoControls.classList.remove('hidden');
                }
                else {
                    this.video.controls = true;
                    this.videoControls.classList.add('hidden');
                }
            }
            else {
                this.video.controls = false;
                this.videoControls.classList.add('hidden');
            }
        };
        this.updatePlayButton = () => {
            const svg = this.playButton.getElementsByClassName('playback-icons')[0];
            const shortcut = descShortcut(this.options.shortcuts.play);
            if (this.video.paused || this.video.ended) {
                iconShow(svg, 'play-icon');
                this.playButton.setAttribute('data-title', `Play (${shortcut})`);
            }
            else {
                iconShow(svg, 'pause');
                this.playButton.setAttribute('data-title', `Pause (${shortcut})`);
            }
        };
        this.initializeVideo = () => {
            const videoDuration = Math.floor(this.video.duration);
            this.seek.setAttribute('max', `${videoDuration}`);
            this.progress.setAttribute('max', `${videoDuration}`);
            const time = formatTime(videoDuration);
            this.duration.innerText = `${time.minutes}:${time.seconds}`;
            this.duration.setAttribute('datetime', `${time.minutes}m ${time.seconds}s`);
        };
        // updateTimeElapsed indicates how far through the video
        // the current playback is by updating the timeElapsed element
        this.updateTimeElapsed = () => {
            const time = formatTime(Math.floor(this.video.currentTime));
            this.timeElapsed.innerText = `${time.minutes}:${time.seconds}`;
            this.timeElapsed.setAttribute('datetime', `${time.minutes}m ${time.seconds}s`);
        };
        // updateProgress indicates how far through the video
        // the current playback is by updating the progress bar
        this.updateProgress = () => {
            this.seek.value = `${Math.floor(this.video.currentTime)}`;
            this.progress.value = Math.floor(this.video.currentTime);
        };
        // updateSeekTooltip uses the position of the mouse on the progress bar to
        // roughly work out what point in the video the user will skip to if
        // the progress bar is clicked at that point
        this.updateSeekTooltip = (event) => {
            const skipTo = Math.round((event.offsetX / this.seek.clientWidth) *
                parseInt(this.seek.getAttribute('max') || '0', 10));
            this.seek.setAttribute('data-seek', `${skipTo}`);
            const t = formatTime(skipTo);
            this.seekTooltip.textContent = `${t.minutes}:${t.seconds}`;
            const rect = this.video.getBoundingClientRect();
            this.seekTooltip.style.left = `${event.pageX - rect.left}px`;
        };
        // skipAhead jumps to a different point in the video when the progress bar
        // is clicked
        this.skipAhead = () => {
            const skipTo = this.seek.dataset.seek
                ? this.seek.dataset.seek
                : this.seek.value;
            this.video.currentTime = Number.parseFloat(skipTo);
            this.progress.value = Number.parseFloat(skipTo);
            this.seek.value = skipTo;
        };
        // updateVolume updates the video's volume
        // and disables the muted state if active
        this.updateVolume = () => {
            if (this.video.muted) {
                this.video.muted = false;
            }
            this.video.volume = Number.parseFloat(this.volume.value);
        };
        // updateVolumeIcon updates the volume icon so that it correctly reflects
        // the volume of the video
        this.updateVolumeIcon = () => {
            const shortcut = descShortcut(this.options.shortcuts.mute);
            this.volumeButton.setAttribute('data-title', `Mute (${shortcut})`);
            if (this.video.muted || this.video.volume === 0) {
                this.volumeButton.setAttribute('data-title', `Unmute (${shortcut})`);
                iconShow(this.volumeIcons, 'volume-mute');
            }
            else if (this.video.volume > 0 && this.video.volume <= 0.5) {
                iconShow(this.volumeIcons, 'volume-low');
            }
            else {
                iconShow(this.volumeIcons, 'volume-high');
            }
        };
        // toggleMute mutes or unmutes the video when executed
        // When the video is unmuted, the volume is returned to the value
        // it was set to before the video was muted
        this.toggleMute = () => {
            this.video.muted = !this.video.muted;
            if (this.video.muted) {
                this.volume.setAttribute('data-volume', this.volume.value);
                this.volume.value = '0';
            }
            else {
                this.volume.value = this.volume.dataset.volume || `${this.video.volume}`;
            }
        };
        // animatePlayback displays an animation when
        // the video is played or paused
        this.animatePlayback = () => {
            this.playbackAnimation.animate([
                {
                    opacity: 1,
                    transform: 'scale(1)',
                },
                {
                    opacity: 0,
                    transform: 'scale(1.3)',
                },
            ], {
                duration: 500,
            });
        };
        // toggleFullScreen toggles the full screen state of the video
        // If the browser is currently in fullscreen mode,
        // then it should exit and vice versa.
        this.toggleFullScreen = () => {
            if (document.fullscreenElement) {
                document.exitFullscreen();
            }
            else if (document.webkitFullscreenElement) {
                // Need this to support Safari
                document.webkitExitFullscreen();
            }
            else if (this.container.webkitRequestFullscreen) {
                // Need this to support Safari
                this.container.webkitRequestFullscreen();
            }
            else {
                this.container.requestFullscreen();
            }
        };
        this.isFullscreen = () => {
            return (document.fullscreenElement ||
                document.webkitFullscreenElement ||
                this.container.webkitRequestFullscreen);
        };
        // updateFullscreenButton changes the icon of the full screen button
        // and tooltip to reflect the current full screen state of the video
        this.updateFullscreenButton = () => {
            const shortcut = descShortcut(this.options.shortcuts.fullscreen);
            if (this.isFullscreen()) {
                this.fullscreenButton.setAttribute('data-title', `Exit full screen (${shortcut})`);
                iconShow(this.fullscreenIcons, 'fullscreen-exit');
            }
            else {
                this.fullscreenButton.setAttribute('data-title', `Full screen (${shortcut})`);
                iconShow(this.fullscreenIcons, 'fullscreen');
            }
        };
        // togglePip toggles Picture-in-Picture mode on the video
        this.togglePip = () => __awaiter(this, void 0, void 0, function* () {
            try {
                if (this.video !== document.pictureInPictureElement) {
                    this.pipButton.disabled = true;
                    yield this.video.requestPictureInPicture();
                }
                else {
                    yield document.exitPictureInPicture();
                }
            }
            catch (error) {
                console.error(error);
            }
            finally {
                this.pipButton.disabled = false;
            }
        });
        // hideControls hides the video controls when not in use
        // if the video is paused, the controls must remain visible
        this.hideControls = () => {
            if (this.video.paused) {
                return;
            }
            this.videoControls.classList.add('hide');
        };
        // showControls displays the video controls
        this.showControls = () => {
            this.videoControls.classList.remove('hide');
        };
        this.isInFocus = () => {
            var _a;
            return ((_a = document.activeElement) === null || _a === void 0 ? void 0 : _a.contains(this.container)) || false;
        };
        // keyboardShortcuts executes the relevant functions for
        // each supported shortcut key
        this.keyboardShortcuts = (event) => {
            if (!this.isInFocus()) {
                return;
            }
            const { key, ctrlKey, altKey, shiftKey } = event;
            const { play, mute, fullscreen, pip } = this.options.shortcuts;
            if (key === play.key &&
                (play.ctrl === !!ctrlKey ||
                    play.alt === !!altKey ||
                    play.shift === !!shiftKey)) {
                this.togglePlay();
                this.animatePlayback();
                if (this.video.paused) {
                    this.showControls();
                }
                else {
                    setTimeout(() => {
                        this.hideControls();
                    }, 2000);
                }
            }
            else if (key === mute.key &&
                (mute.ctrl === !!ctrlKey ||
                    mute.alt === !!altKey ||
                    mute.shift === !!shiftKey)) {
                this.toggleMute();
            }
            else if (key === fullscreen.key &&
                (fullscreen.ctrl === !!ctrlKey ||
                    fullscreen.alt === !!altKey ||
                    fullscreen.shift === !!shiftKey)) {
                this.toggleFullScreen();
            }
            else if (key === pip.key &&
                (pip.ctrl === !!ctrlKey ||
                    pip.alt === !!altKey ||
                    pip.shift === !!shiftKey)) {
                this.togglePip();
            }
        };
        this.options = makeOptions(opts);
        this.installSvg();
        this.container = createVideoContainer(this.options);
        this.video = this.container.querySelector('video.video');
        this.videoControls = this.container.querySelector('div.video-controls');
        this.playButton = this.container.querySelector('button.play');
        this.timeElapsed = this.container.querySelector('time.time-elapsed');
        this.duration = this.container.querySelector('time.duration');
        this.progress = this.container.querySelector('progress.progress-bar');
        this.seek = this.container.querySelector('input.seek');
        this.seekTooltip = this.container.querySelector('div.seek-tooltip');
        this.volume = this.container.querySelector('input.volume');
        this.volumeButton = this.container.querySelector('button.volume-button');
        this.volumeIcons = this.volumeButton.querySelector('svg');
        this.playbackAnimation = this.container.querySelector('div.playback-animation');
        this.fullscreenButton = this.container.querySelector('button.fullscreen-button');
        this.fullscreenIcons = this.fullscreenButton.querySelector('svg');
        this.pipButton = this.container.querySelector('button.pip-button');
        this.indexSelector = this.container.querySelector('button.index-selector');
        this.playButton.addEventListener('click', this.togglePlay);
        this.video.addEventListener('play', this.updatePlayButton);
        this.video.addEventListener('pause', this.updatePlayButton);
        this.video.addEventListener('loadedmetadata', this.initializeVideo);
        this.video.addEventListener('timeupdate', this.updateTimeElapsed);
        this.video.addEventListener('timeupdate', this.updateProgress);
        this.video.addEventListener('volumechange', this.updateVolumeIcon);
        this.video.addEventListener('click', this.togglePlay);
        this.video.addEventListener('click', this.animatePlayback);
        this.video.addEventListener('mouseenter', this.showControls);
        this.video.addEventListener('mouseleave', this.hideControls);
        this.videoControls.addEventListener('mouseenter', this.showControls);
        this.videoControls.addEventListener('mouseleave', this.hideControls);
        this.seek.addEventListener('mousemove', this.updateSeekTooltip);
        this.seek.addEventListener('input', this.skipAhead);
        this.volume.addEventListener('input', this.updateVolume);
        this.volumeButton.addEventListener('click', this.toggleMute);
        this.fullscreenButton.addEventListener('click', this.toggleFullScreen);
        this.container.addEventListener('fullscreenchange', this.updateFullscreenButton);
        this.pipButton.addEventListener('click', this.togglePip);
        document.addEventListener('keyup', this.keyboardShortcuts);
    }
}
exports.Video = Video;
// formatTime takes a time length in seconds and returns the time in
// minutes and seconds
function formatTime(timeInSeconds) {
    const result = new Date(timeInSeconds * 1000).toISOString().substr(11, 8);
    return {
        minutes: result.substr(3, 2),
        seconds: result.substr(6, 2),
    };
}


/***/ }),

/***/ "./src/webcam.ts":
/*!***********************!*\
  !*** ./src/webcam.ts ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Xiaojing Chen
// Distributed under the terms of the Modified BSD License.
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.WebCamView = exports.WebCamModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "@jupyter-widgets/base");
const common_1 = __webpack_require__(/*! ./common */ "./src/common.ts");
const webrtc_1 = __webpack_require__(/*! ./webrtc */ "./src/webrtc.ts");
const utils_1 = __webpack_require__(/*! ./utils */ "./src/utils.ts");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
const supportsSetCodecPreferences = window.RTCRtpTransceiver &&
    'setCodecPreferences' in window.RTCRtpTransceiver.prototype;
class WebCamModel extends common_1.BaseModel {
    // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
    constructor(...args) {
        super(...args);
        this.getDevice = (type) => __awaiter(this, void 0, void 0, function* () {
            const stream = yield navigator.mediaDevices.getUserMedia({
                video: type === 'video_input',
                audio: type === 'audio_input' || type === 'audio_output',
            });
            try {
                const n_type = type.replace('_', '');
                const devices = yield navigator.mediaDevices.enumerateDevices();
                return devices.filter((device) => device.kind === n_type && device.deviceId);
            }
            finally {
                stream.getTracks().forEach((track) => track.stop());
            }
        });
        this.resetPeer = () => {
            this.pc = undefined;
            this.client_stream = undefined;
            this.server_stream = undefined;
        };
        this.waitForStateWhen = (checker) => __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve) => {
                const state = this.get('state');
                if (checker(state)) {
                    resolve(state);
                }
                else {
                    const checkState = () => {
                        const state = this.get('state');
                        if (checker(state)) {
                            this.off('change:state', checkState);
                            resolve(state);
                        }
                    };
                    this.on('change:state', checkState);
                }
            });
        });
        this.waitForStateIn = (...states) => __awaiter(this, void 0, void 0, function* () {
            return this.waitForStateWhen((state) => states.indexOf(state) !== -1);
        });
        this.getState = () => this.get('state');
        this.setState = (state) => {
            this.set('state', state);
        };
        this.getConstraints = () => {
            let { video, audio } = this.get('constraints') || { audio: false, video: true };
            const videoId = this.videoInput;
            const audioId = this.audioInput;
            if (audio && audioId) {
                if (typeof audio === 'boolean') {
                    audio = {
                        deviceId: audioId,
                    };
                }
                else {
                    audio.deviceId = audioId;
                }
            }
            if (video && videoId) {
                if (typeof video === 'boolean') {
                    video = {
                        deviceId: videoId,
                    };
                }
                else {
                    video.deviceId = videoId;
                }
            }
            return { video, audio };
        };
        this.closePeer = () => __awaiter(this, void 0, void 0, function* () {
            const state = yield this.waitForStateIn('closed', 'connected', 'error', 'new', 'error');
            if (state === 'new') {
                throw new Error(`This should not happen. We can't close the peer when the state is ${state}. Because at this time, we haven't start the peer.`);
            }
            if (state === 'closed' || state === 'error') {
                return;
            }
            const pc = this.pc;
            if (!pc) {
                this.setState('closed');
                return;
            }
            this.setState('closing');
            try {
                pc.close();
                if (pc.connectionState !== 'closed') {
                    yield new Promise((resolve) => {
                        pc.addEventListener('connectionstatechange', () => {
                            if (pc.connectionState === 'closed') {
                                resolve();
                            }
                        });
                    });
                }
                this.resetPeer();
                this.setState('closed');
            }
            catch (err) {
                this.setState('error');
            }
        });
        this.fetchCodecs = () => {
            const codecs = this.getCodecs();
            this.set('video_codecs', codecs);
            this.save_changes();
        };
        this.getCodecs = () => {
            if (supportsSetCodecPreferences) {
                const { codecs = [] } = RTCRtpSender.getCapabilities('video') || {};
                return codecs
                    .filter((codec) => !utils_1.arrayInclude(['video/red', 'video/ulpfec', 'video/rtx'], codec.mimeType))
                    .map((codec) => {
                    return (codec.mimeType + ' ' + (codec.sdpFmtpLine || '')).trim();
                });
            }
            else {
                return [];
            }
        };
        this.getPeerConfig = () => {
            const config = {};
            const iceServers = this.get('iceServers');
            if (iceServers && iceServers.length > 0) {
                config.iceServers = iceServers.map((server) => {
                    if (typeof server === 'string') {
                        return { urls: server };
                    }
                    else {
                        return server;
                    }
                });
            }
            return config;
        };
        this.syncDevice = (track) => {
            const type = track.kind === 'video' ? 'video_input' : 'audio_input';
            let curDeviceId;
            if (typeof track.getCapabilities !== 'undefined') {
                curDeviceId = track.getCapabilities().deviceId;
            }
            else {
                curDeviceId = track.getSettings().deviceId;
            }
            if (type === 'video_input') {
                this.videoInput = curDeviceId;
            }
            else {
                this.audioInput = curDeviceId;
            }
            this.send_cmd('sync_device', { type, id: curDeviceId }, false);
        };
        this.connect = (video, force_reconnect = false, only_reconnect = false) => __awaiter(this, void 0, void 0, function* () {
            const state = yield this.waitForStateIn('closed', 'connected', 'error', 'new');
            if (state === 'closed' || state === 'error' || state === 'new') {
                if (only_reconnect) {
                    return;
                }
                try {
                    this.setState('connecting');
                    const pc = webrtc_1.createPeerConnection(this.getPeerConfig());
                    this.pc = pc;
                    this.bindVideo(video);
                    pc.addEventListener('connectionstatechange', () => {
                        const state = pc.connectionState;
                        if (state === 'failed' ||
                            state === 'disconnected' ||
                            state === 'closed') {
                            pc.close();
                            if (this.pc === pc) {
                                this.resetPeer();
                            }
                        }
                    });
                    pc.addEventListener('track', (evt) => {
                        if (evt.track.kind === 'video') {
                            console.log('track gotten');
                            this.server_stream = evt.streams[0];
                        }
                    });
                    const stream = yield navigator.mediaDevices.getUserMedia(this.getConstraints());
                    this.client_stream = stream;
                    stream.getTracks().forEach((track) => {
                        this.syncDevice(track);
                        pc.addTrack(track, stream);
                    });
                    yield webrtc_1.negotiate(pc, (offer) => __awaiter(this, void 0, void 0, function* () {
                        console.log(offer);
                        const { content } = yield this.send_cmd('exchange_peer', {
                            desc: offer,
                        });
                        return content;
                    }));
                    const pcState = yield webrtc_1.waitForConnectionState(pc, (state) => state !== 'connecting' && state !== 'new');
                    if (pcState === 'connected') {
                        this.setState('connected');
                    }
                    else {
                        yield this.closePeer();
                    }
                }
                catch (err) {
                    this.setState('error');
                    console.error(err);
                }
            }
            else if (force_reconnect) {
                yield this.closePeer();
                yield this.connect(video, force_reconnect);
            }
            else {
                this.bindVideo(video);
            }
        });
        this.bindVideo = (video) => {
            const pc = this.pc;
            if (!pc || !video) {
                return;
            }
            if (pc.connectionState === 'connected' && this.server_stream) {
                video.srcObject = this.server_stream;
            }
            else {
                const handler = (evt) => {
                    if (evt.track.kind === 'video') {
                        console.log('track gotten');
                        this.server_stream = evt.streams[0];
                        video.srcObject = this.server_stream;
                        pc.removeEventListener('track', handler);
                    }
                };
                pc.addEventListener('track', handler);
            }
        };
        this.fetchCodecs();
        // this.fetchDevices();
        // this.on('change:video_input_device', (...args) => {
        //   console.log('change:video_input_device');
        //   console.log(args);
        //   this.connect(undefined, true, true);
        // });
        // this.on('change:audio_input_device', (...args) => {
        //   console.log('change:audio_input_device');
        //   console.log(args);
        //   this.connect(undefined, true, true);
        // });
        this.on('change:iceServers', () => {
            this.connect(undefined, true, true);
        });
        this.addMessageHandler('request_devices', (cmdMsg) => {
            const { cmd, id, args } = cmdMsg;
            const { type } = args;
            this.getDevice(type).then((devices) => {
                console.log(devices);
                this.send({ ans: cmd, id, res: devices }, {});
            });
        });
        this.addMessageHandler('notify_device_change', (cmdMsg) => {
            const { args } = cmdMsg;
            const { type, change } = args;
            if (type === 'video_input') {
                if (this.videoInput !== change.new) {
                    this.videoInput = change.new;
                    this.connect(undefined, true, true);
                }
            }
            else if (type === 'audio_input') {
                if (this.audioInput !== change.new) {
                    this.audioInput = change.new;
                    this.connect(undefined, true, true);
                }
            }
        });
    }
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: WebCamModel.model_name, _view_name: WebCamModel.view_name, server_desc: null, client_desc: null, iceServers: [], constraints: null, video_codecs: [], video_codec: null, state: 'new', autoplay: true, controls: true, crossOrigin: 'not-support', width: null, height: null, playsInline: true, muted: false });
    }
}
exports.WebCamModel = WebCamModel;
WebCamModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
WebCamModel.model_name = 'WebCamModel';
WebCamModel.view_name = 'WebCamView'; // Set to null if no view
function attachSinkId(element, sinkId) {
    return __awaiter(this, void 0, void 0, function* () {
        if (typeof element.sinkId !== 'undefined') {
            if (sinkId) {
                yield element.setSinkId(sinkId);
            }
        }
        else {
            console.warn('Browser does not support output device selection.');
        }
    });
}
class WebCamView extends base_1.DOMWidgetView {
    render() {
        const video = document.createElement('video');
        video.playsInline = true;
        this.el.appendChild(video);
        this.model.connect(video);
        this.model.on('change:state', () => {
            const model = this.model;
            if (model.getState() === 'connected') {
                model.connect(video);
            }
        });
        const { deviceId } = this.model.get('audio_output_device') || {};
        attachSinkId(video, deviceId);
        this.model.on('change:audio_output_device', () => {
            const { deviceId } = this.model.get('audio_output_device') || {};
            attachSinkId(video, deviceId);
        });
        video.autoplay = this.model.get('autoplay');
        this.model.on('change:autoplay', () => {
            video.autoplay = this.model.get('autoplay');
        });
        video.controls = this.model.get('controls');
        this.model.on('change:controls', () => {
            video.controls = this.model.get('controls');
        });
        const width = this.model.get('width');
        if (width) {
            video.width = width;
        }
        this.model.on('change:width', () => {
            const width = this.model.get('width');
            if (width) {
                video.width = width;
            }
            else {
                video.removeAttribute('width');
            }
        });
        const height = this.model.get('height');
        if (height) {
            video.height = height;
        }
        this.model.on('change:height', () => {
            const height = this.model.get('height');
            if (height) {
                video.height = height;
            }
            else {
                video.removeAttribute('height');
            }
        });
        video.playsInline = this.model.get('playsInline');
        this.model.on('change:playsInline', () => {
            video.playsInline = this.model.get('playsInline');
        });
        video.muted = this.model.get('muted');
        this.model.on('change:muted', () => {
            video.muted = this.model.get('muted');
        });
        const crossOrigin = this.model.get('crossOrigin');
        if (crossOrigin === 'not-support') {
            video.crossOrigin = null;
        }
        else {
            video.crossOrigin = crossOrigin;
        }
        this.model.on('change:crossOrigin', () => {
            const crossOrigin = this.model.get('crossOrigin');
            if (crossOrigin === 'not-support') {
                video.crossOrigin = null;
            }
            else {
                video.crossOrigin = crossOrigin;
            }
        });
    }
}
exports.WebCamView = WebCamView;


/***/ }),

/***/ "./src/webrtc.ts":
/*!***********************!*\
  !*** ./src/webrtc.ts ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

/* eslint-disable @typescript-eslint/no-non-null-assertion */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.negotiate = exports.waitForConnectionState = exports.createPeerConnection = void 0;
const utils_1 = __webpack_require__(/*! ./utils */ "./src/utils.ts");
const DEFAULT_ICE_SERVERS = [
    { urls: ['stun:stun.l.google.com:19302'] },
    { urls: ['stun:23.21.150.121'] },
    { urls: ['stun:stun01.sipphone.com'] },
    { urls: ['stun:stun.ekiga.net'] },
    { urls: ['stun:stun.fwdnet.net'] },
    { urls: ['stun:stun.ideasip.com'] },
    { urls: ['stun:stun.iptel.org'] },
    { urls: ['stun:stun.rixtelecom.se'] },
    { urls: ['stun:stun.schlund.de'] },
    { urls: ['stun:stunserver.org'] },
    { urls: ['stun:stun.softjoys.com'] },
    { urls: ['stun:stun.voiparound.com'] },
    { urls: ['stun:stun.voipbuster.com'] },
    { urls: ['stun:stun.voipstunt.com'] },
    { urls: ['stun:stun.voxgratia.org'] },
    { urls: ['stun:stun.xten.com'] },
];
function createPeerConnection(config) {
    const pc = new RTCPeerConnection(Object.assign({}, { iceServers: DEFAULT_ICE_SERVERS }, config || {}));
    pc.addEventListener('connectionstatechange', () => {
        console.log(`connection -> ${pc.connectionState}`);
    }, false);
    // register some listeners to help debugging
    pc.addEventListener('icegatheringstatechange', () => {
        console.log(`iceGathering -> ${pc.iceGatheringState}`);
    }, false);
    pc.addEventListener('iceconnectionstatechange', () => {
        console.log(`iceConnection -> ${pc.iceConnectionState}`);
    }, false);
    pc.addEventListener('signalingstatechange', () => {
        console.log(`signaling -> ${pc.signalingState}`);
    }, false);
    return pc;
}
exports.createPeerConnection = createPeerConnection;
function waitForConnectionState(pc, checker) {
    return __awaiter(this, void 0, void 0, function* () {
        return new Promise((resolve) => {
            if (checker(pc.connectionState)) {
                resolve(pc.connectionState);
            }
            else {
                const checkState = () => {
                    if (checker(pc.connectionState)) {
                        pc.removeEventListener('connectionstatechange', checkState);
                        resolve(pc.connectionState);
                    }
                };
                pc.addEventListener('connectionstatechange', checkState);
            }
        });
    });
}
exports.waitForConnectionState = waitForConnectionState;
function waitIceGathering(pc) {
    return __awaiter(this, void 0, void 0, function* () {
        return new Promise((resolve) => {
            if (pc.iceGatheringState === 'complete') {
                resolve();
            }
            else {
                const checkState = () => {
                    if (pc.iceGatheringState === 'complete') {
                        pc.removeEventListener('icegatheringstatechange', checkState);
                        resolve();
                    }
                };
                pc.addEventListener('icegatheringstatechange', checkState);
            }
        });
    });
}
function negotiate(pc, answerFunc, codec) {
    return __awaiter(this, void 0, void 0, function* () {
        let offer = yield pc.createOffer();
        yield pc.setLocalDescription(offer);
        yield waitIceGathering(pc);
        offer = pc.localDescription;
        if (codec) {
            if (codec.audio && codec.audio !== 'default') {
                offer.sdp = sdpFilterCodec('audio', codec.audio, offer.sdp);
            }
            if (codec.video && codec.video !== 'default') {
                offer.sdp = sdpFilterCodec('video', codec.video, offer.sdp);
            }
        }
        const answer = yield answerFunc(offer);
        yield pc.setRemoteDescription(answer);
    });
}
exports.negotiate = negotiate;
function sdpFilterCodec(kind, codec, realSdp) {
    const allowed = [];
    const rtxRegex = new RegExp('a=fmtp:(\\d+) apt=(\\d+)\\r$');
    const codecRegex = new RegExp('a=rtpmap:([0-9]+) ' + escapeRegExp(codec));
    const videoRegex = new RegExp('(m=' + kind + ' .*?)( ([0-9]+))*\\s*$');
    const lines = realSdp.split('\n');
    let isKind = false;
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].startsWith('m=' + kind + ' ')) {
            isKind = true;
        }
        else if (lines[i].startsWith('m=')) {
            isKind = false;
        }
        if (isKind) {
            let match = lines[i].match(codecRegex);
            if (match) {
                allowed.push(parseInt(match[1]));
            }
            match = lines[i].match(rtxRegex);
            if (match && utils_1.arrayInclude(allowed, parseInt(match[2]))) {
                allowed.push(parseInt(match[1]));
            }
        }
    }
    const skipRegex = 'a=(fmtp|rtcp-fb|rtpmap):([0-9]+)';
    let sdp = '';
    isKind = false;
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].startsWith('m=' + kind + ' ')) {
            isKind = true;
        }
        else if (lines[i].startsWith('m=')) {
            isKind = false;
        }
        if (isKind) {
            const skipMatch = lines[i].match(skipRegex);
            if (skipMatch && !utils_1.arrayInclude(allowed, parseInt(skipMatch[2]))) {
                continue;
            }
            else if (lines[i].match(videoRegex)) {
                sdp += lines[i].replace(videoRegex, '$1 ' + allowed.join(' ')) + '\n';
            }
            else {
                sdp += lines[i] + '\n';
            }
        }
        else {
            sdp += lines[i] + '\n';
        }
    }
    return sdp;
}
function escapeRegExp(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}


/***/ }),

/***/ "@jupyter-widgets/base":
/*!****************************************!*\
  !*** external "@jupyter-widgets/base" ***!
  \****************************************/
/***/ ((module) => {

"use strict";
module.exports = __WEBPACK_EXTERNAL_MODULE__jupyter_widgets_base__;

/***/ }),

/***/ "./node_modules/lru-cache/index.js":
/*!*****************************************!*\
  !*** ./node_modules/lru-cache/index.js ***!
  \*****************************************/
/***/ ((module) => {

const perf =
  typeof performance === 'object' &&
  performance &&
  typeof performance.now === 'function'
    ? performance
    : Date

const hasAbortController = typeof AbortController === 'function'

// minimal backwards-compatibility polyfill
// this doesn't have nearly all the checks and whatnot that
// actual AbortController/Signal has, but it's enough for
// our purposes, and if used properly, behaves the same.
const AC = hasAbortController
  ? AbortController
  : class AbortController {
      constructor() {
        this.signal = new AS()
      }
      abort() {
        this.signal.dispatchEvent({
          type: 'abort',
          target: this.signal,
        })
      }
    }

const hasAbortSignal = typeof AbortSignal === 'function'
// Some polyfills put this on the AC class, not global
const hasACAbortSignal = typeof AC.AbortSignal === 'function'
const AS = hasAbortSignal
  ? AbortSignal
  : hasACAbortSignal
  ? AC.AbortController
  : class AbortSignal {
      constructor() {
        this.aborted = false
        this._listeners = []
      }
      dispatchEvent(e) {
        if (e.type === 'abort') {
          this.aborted = true
          this.onabort(e)
          this._listeners.forEach(f => f(e), this)
        }
      }
      onabort() {}
      addEventListener(ev, fn) {
        if (ev === 'abort') {
          this._listeners.push(fn)
        }
      }
      removeEventListener(ev, fn) {
        if (ev === 'abort') {
          this._listeners = this._listeners.filter(f => f !== fn)
        }
      }
    }

const warned = new Set()
const deprecatedOption = (opt, instead) => {
  const code = `LRU_CACHE_OPTION_${opt}`
  if (shouldWarn(code)) {
    warn(code, `${opt} option`, `options.${instead}`, LRUCache)
  }
}
const deprecatedMethod = (method, instead) => {
  const code = `LRU_CACHE_METHOD_${method}`
  if (shouldWarn(code)) {
    const { prototype } = LRUCache
    const { get } = Object.getOwnPropertyDescriptor(prototype, method)
    warn(code, `${method} method`, `cache.${instead}()`, get)
  }
}
const deprecatedProperty = (field, instead) => {
  const code = `LRU_CACHE_PROPERTY_${field}`
  if (shouldWarn(code)) {
    const { prototype } = LRUCache
    const { get } = Object.getOwnPropertyDescriptor(prototype, field)
    warn(code, `${field} property`, `cache.${instead}`, get)
  }
}

const emitWarning = (...a) => {
  typeof process === 'object' &&
  process &&
  typeof process.emitWarning === 'function'
    ? process.emitWarning(...a)
    : console.error(...a)
}

const shouldWarn = code => !warned.has(code)

const warn = (code, what, instead, fn) => {
  warned.add(code)
  const msg = `The ${what} is deprecated. Please use ${instead} instead.`
  emitWarning(msg, 'DeprecationWarning', code, fn)
}

const isPosInt = n => n && n === Math.floor(n) && n > 0 && isFinite(n)

/* istanbul ignore next - This is a little bit ridiculous, tbh.
 * The maximum array length is 2^32-1 or thereabouts on most JS impls.
 * And well before that point, you're caching the entire world, I mean,
 * that's ~32GB of just integers for the next/prev links, plus whatever
 * else to hold that many keys and values.  Just filling the memory with
 * zeroes at init time is brutal when you get that big.
 * But why not be complete?
 * Maybe in the future, these limits will have expanded. */
const getUintArray = max =>
  !isPosInt(max)
    ? null
    : max <= Math.pow(2, 8)
    ? Uint8Array
    : max <= Math.pow(2, 16)
    ? Uint16Array
    : max <= Math.pow(2, 32)
    ? Uint32Array
    : max <= Number.MAX_SAFE_INTEGER
    ? ZeroArray
    : null

class ZeroArray extends Array {
  constructor(size) {
    super(size)
    this.fill(0)
  }
}

class Stack {
  constructor(max) {
    if (max === 0) {
      return []
    }
    const UintArray = getUintArray(max)
    this.heap = new UintArray(max)
    this.length = 0
  }
  push(n) {
    this.heap[this.length++] = n
  }
  pop() {
    return this.heap[--this.length]
  }
}

class LRUCache {
  constructor(options = {}) {
    const {
      max = 0,
      ttl,
      ttlResolution = 1,
      ttlAutopurge,
      updateAgeOnGet,
      updateAgeOnHas,
      allowStale,
      dispose,
      disposeAfter,
      noDisposeOnSet,
      noUpdateTTL,
      maxSize = 0,
      maxEntrySize = 0,
      sizeCalculation,
      fetchMethod,
      fetchContext,
      noDeleteOnFetchRejection,
      noDeleteOnStaleGet,
      allowStaleOnFetchRejection,
    } = options

    // deprecated options, don't trigger a warning for getting them if
    // the thing being passed in is another LRUCache we're copying.
    const { length, maxAge, stale } =
      options instanceof LRUCache ? {} : options

    if (max !== 0 && !isPosInt(max)) {
      throw new TypeError('max option must be a nonnegative integer')
    }

    const UintArray = max ? getUintArray(max) : Array
    if (!UintArray) {
      throw new Error('invalid max value: ' + max)
    }

    this.max = max
    this.maxSize = maxSize
    this.maxEntrySize = maxEntrySize || this.maxSize
    this.sizeCalculation = sizeCalculation || length
    if (this.sizeCalculation) {
      if (!this.maxSize && !this.maxEntrySize) {
        throw new TypeError(
          'cannot set sizeCalculation without setting maxSize or maxEntrySize'
        )
      }
      if (typeof this.sizeCalculation !== 'function') {
        throw new TypeError('sizeCalculation set to non-function')
      }
    }

    this.fetchMethod = fetchMethod || null
    if (this.fetchMethod && typeof this.fetchMethod !== 'function') {
      throw new TypeError(
        'fetchMethod must be a function if specified'
      )
    }

    this.fetchContext = fetchContext
    if (!this.fetchMethod && fetchContext !== undefined) {
      throw new TypeError(
        'cannot set fetchContext without fetchMethod'
      )
    }

    this.keyMap = new Map()
    this.keyList = new Array(max).fill(null)
    this.valList = new Array(max).fill(null)
    this.next = new UintArray(max)
    this.prev = new UintArray(max)
    this.head = 0
    this.tail = 0
    this.free = new Stack(max)
    this.initialFill = 1
    this.size = 0

    if (typeof dispose === 'function') {
      this.dispose = dispose
    }
    if (typeof disposeAfter === 'function') {
      this.disposeAfter = disposeAfter
      this.disposed = []
    } else {
      this.disposeAfter = null
      this.disposed = null
    }
    this.noDisposeOnSet = !!noDisposeOnSet
    this.noUpdateTTL = !!noUpdateTTL
    this.noDeleteOnFetchRejection = !!noDeleteOnFetchRejection
    this.allowStaleOnFetchRejection = !!allowStaleOnFetchRejection

    // NB: maxEntrySize is set to maxSize if it's set
    if (this.maxEntrySize !== 0) {
      if (this.maxSize !== 0) {
        if (!isPosInt(this.maxSize)) {
          throw new TypeError(
            'maxSize must be a positive integer if specified'
          )
        }
      }
      if (!isPosInt(this.maxEntrySize)) {
        throw new TypeError(
          'maxEntrySize must be a positive integer if specified'
        )
      }
      this.initializeSizeTracking()
    }

    this.allowStale = !!allowStale || !!stale
    this.noDeleteOnStaleGet = !!noDeleteOnStaleGet
    this.updateAgeOnGet = !!updateAgeOnGet
    this.updateAgeOnHas = !!updateAgeOnHas
    this.ttlResolution =
      isPosInt(ttlResolution) || ttlResolution === 0
        ? ttlResolution
        : 1
    this.ttlAutopurge = !!ttlAutopurge
    this.ttl = ttl || maxAge || 0
    if (this.ttl) {
      if (!isPosInt(this.ttl)) {
        throw new TypeError(
          'ttl must be a positive integer if specified'
        )
      }
      this.initializeTTLTracking()
    }

    // do not allow completely unbounded caches
    if (this.max === 0 && this.ttl === 0 && this.maxSize === 0) {
      throw new TypeError(
        'At least one of max, maxSize, or ttl is required'
      )
    }
    if (!this.ttlAutopurge && !this.max && !this.maxSize) {
      const code = 'LRU_CACHE_UNBOUNDED'
      if (shouldWarn(code)) {
        warned.add(code)
        const msg =
          'TTL caching without ttlAutopurge, max, or maxSize can ' +
          'result in unbounded memory consumption.'
        emitWarning(msg, 'UnboundedCacheWarning', code, LRUCache)
      }
    }

    if (stale) {
      deprecatedOption('stale', 'allowStale')
    }
    if (maxAge) {
      deprecatedOption('maxAge', 'ttl')
    }
    if (length) {
      deprecatedOption('length', 'sizeCalculation')
    }
  }

  getRemainingTTL(key) {
    return this.has(key, { updateAgeOnHas: false }) ? Infinity : 0
  }

  initializeTTLTracking() {
    this.ttls = new ZeroArray(this.max)
    this.starts = new ZeroArray(this.max)

    this.setItemTTL = (index, ttl, start = perf.now()) => {
      this.starts[index] = ttl !== 0 ? start : 0
      this.ttls[index] = ttl
      if (ttl !== 0 && this.ttlAutopurge) {
        const t = setTimeout(() => {
          if (this.isStale(index)) {
            this.delete(this.keyList[index])
          }
        }, ttl + 1)
        /* istanbul ignore else - unref() not supported on all platforms */
        if (t.unref) {
          t.unref()
        }
      }
    }

    this.updateItemAge = index => {
      this.starts[index] = this.ttls[index] !== 0 ? perf.now() : 0
    }

    // debounce calls to perf.now() to 1s so we're not hitting
    // that costly call repeatedly.
    let cachedNow = 0
    const getNow = () => {
      const n = perf.now()
      if (this.ttlResolution > 0) {
        cachedNow = n
        const t = setTimeout(
          () => (cachedNow = 0),
          this.ttlResolution
        )
        /* istanbul ignore else - not available on all platforms */
        if (t.unref) {
          t.unref()
        }
      }
      return n
    }

    this.getRemainingTTL = key => {
      const index = this.keyMap.get(key)
      if (index === undefined) {
        return 0
      }
      return this.ttls[index] === 0 || this.starts[index] === 0
        ? Infinity
        : this.starts[index] +
            this.ttls[index] -
            (cachedNow || getNow())
    }

    this.isStale = index => {
      return (
        this.ttls[index] !== 0 &&
        this.starts[index] !== 0 &&
        (cachedNow || getNow()) - this.starts[index] >
          this.ttls[index]
      )
    }
  }
  updateItemAge(index) {}
  setItemTTL(index, ttl, start) {}
  isStale(index) {
    return false
  }

  initializeSizeTracking() {
    this.calculatedSize = 0
    this.sizes = new ZeroArray(this.max)
    this.removeItemSize = index => {
      this.calculatedSize -= this.sizes[index]
      this.sizes[index] = 0
    }
    this.requireSize = (k, v, size, sizeCalculation) => {
      // provisionally accept background fetches.
      // actual value size will be checked when they return.
      if (this.isBackgroundFetch(v)) {
        return 0
      }
      if (!isPosInt(size)) {
        if (sizeCalculation) {
          if (typeof sizeCalculation !== 'function') {
            throw new TypeError('sizeCalculation must be a function')
          }
          size = sizeCalculation(v, k)
          if (!isPosInt(size)) {
            throw new TypeError(
              'sizeCalculation return invalid (expect positive integer)'
            )
          }
        } else {
          throw new TypeError(
            'invalid size value (must be positive integer). ' +
              'When maxSize or maxEntrySize is used, sizeCalculation or size ' +
              'must be set.'
          )
        }
      }
      return size
    }
    this.addItemSize = (index, size) => {
      this.sizes[index] = size
      if (this.maxSize) {
        const maxSize = this.maxSize - this.sizes[index]
        while (this.calculatedSize > maxSize) {
          this.evict(true)
        }
      }
      this.calculatedSize += this.sizes[index]
    }
  }
  removeItemSize(index) {}
  addItemSize(index, size) {}
  requireSize(k, v, size, sizeCalculation) {
    if (size || sizeCalculation) {
      throw new TypeError(
        'cannot set size without setting maxSize or maxEntrySize on cache'
      )
    }
  }

  *indexes({ allowStale = this.allowStale } = {}) {
    if (this.size) {
      for (let i = this.tail; true; ) {
        if (!this.isValidIndex(i)) {
          break
        }
        if (allowStale || !this.isStale(i)) {
          yield i
        }
        if (i === this.head) {
          break
        } else {
          i = this.prev[i]
        }
      }
    }
  }

  *rindexes({ allowStale = this.allowStale } = {}) {
    if (this.size) {
      for (let i = this.head; true; ) {
        if (!this.isValidIndex(i)) {
          break
        }
        if (allowStale || !this.isStale(i)) {
          yield i
        }
        if (i === this.tail) {
          break
        } else {
          i = this.next[i]
        }
      }
    }
  }

  isValidIndex(index) {
    return this.keyMap.get(this.keyList[index]) === index
  }

  *entries() {
    for (const i of this.indexes()) {
      if (!this.isBackgroundFetch(this.valList[i])) {
        yield [this.keyList[i], this.valList[i]]
      }
    }
  }
  *rentries() {
    for (const i of this.rindexes()) {
      if (!this.isBackgroundFetch(this.valList[i])) {
        yield [this.keyList[i], this.valList[i]]
      }
    }
  }

  *keys() {
    for (const i of this.indexes()) {
      if (!this.isBackgroundFetch(this.valList[i])) {
        yield this.keyList[i]
      }
    }
  }
  *rkeys() {
    for (const i of this.rindexes()) {
      if (!this.isBackgroundFetch(this.valList[i])) {
        yield this.keyList[i]
      }
    }
  }

  *values() {
    for (const i of this.indexes()) {
      if (!this.isBackgroundFetch(this.valList[i])) {
        yield this.valList[i]
      }
    }
  }
  *rvalues() {
    for (const i of this.rindexes()) {
      if (!this.isBackgroundFetch(this.valList[i])) {
        yield this.valList[i]
      }
    }
  }

  [Symbol.iterator]() {
    return this.entries()
  }

  find(fn, getOptions = {}) {
    for (const i of this.indexes()) {
      if (fn(this.valList[i], this.keyList[i], this)) {
        return this.get(this.keyList[i], getOptions)
      }
    }
  }

  forEach(fn, thisp = this) {
    for (const i of this.indexes()) {
      fn.call(thisp, this.valList[i], this.keyList[i], this)
    }
  }

  rforEach(fn, thisp = this) {
    for (const i of this.rindexes()) {
      fn.call(thisp, this.valList[i], this.keyList[i], this)
    }
  }

  get prune() {
    deprecatedMethod('prune', 'purgeStale')
    return this.purgeStale
  }

  purgeStale() {
    let deleted = false
    for (const i of this.rindexes({ allowStale: true })) {
      if (this.isStale(i)) {
        this.delete(this.keyList[i])
        deleted = true
      }
    }
    return deleted
  }

  dump() {
    const arr = []
    for (const i of this.indexes({ allowStale: true })) {
      const key = this.keyList[i]
      const v = this.valList[i]
      const value = this.isBackgroundFetch(v)
        ? v.__staleWhileFetching
        : v
      if (value === undefined) continue
      const entry = { value }
      if (this.ttls) {
        entry.ttl = this.ttls[i]
        // always dump the start relative to a portable timestamp
        // it's ok for this to be a bit slow, it's a rare operation.
        const age = perf.now() - this.starts[i]
        entry.start = Math.floor(Date.now() - age)
      }
      if (this.sizes) {
        entry.size = this.sizes[i]
      }
      arr.unshift([key, entry])
    }
    return arr
  }

  load(arr) {
    this.clear()
    for (const [key, entry] of arr) {
      if (entry.start) {
        // entry.start is a portable timestamp, but we may be using
        // node's performance.now(), so calculate the offset.
        // it's ok for this to be a bit slow, it's a rare operation.
        const age = Date.now() - entry.start
        entry.start = perf.now() - age
      }
      this.set(key, entry.value, entry)
    }
  }

  dispose(v, k, reason) {}

  set(
    k,
    v,
    {
      ttl = this.ttl,
      start,
      noDisposeOnSet = this.noDisposeOnSet,
      size = 0,
      sizeCalculation = this.sizeCalculation,
      noUpdateTTL = this.noUpdateTTL,
    } = {}
  ) {
    size = this.requireSize(k, v, size, sizeCalculation)
    // if the item doesn't fit, don't do anything
    // NB: maxEntrySize set to maxSize by default
    if (this.maxEntrySize && size > this.maxEntrySize) {
      // have to delete, in case a background fetch is there already.
      // in non-async cases, this is a no-op
      this.delete(k)
      return this
    }
    let index = this.size === 0 ? undefined : this.keyMap.get(k)
    if (index === undefined) {
      // addition
      index = this.newIndex()
      this.keyList[index] = k
      this.valList[index] = v
      this.keyMap.set(k, index)
      this.next[this.tail] = index
      this.prev[index] = this.tail
      this.tail = index
      this.size++
      this.addItemSize(index, size)
      noUpdateTTL = false
    } else {
      // update
      this.moveToTail(index)
      const oldVal = this.valList[index]
      if (v !== oldVal) {
        if (this.isBackgroundFetch(oldVal)) {
          oldVal.__abortController.abort()
        } else {
          if (!noDisposeOnSet) {
            this.dispose(oldVal, k, 'set')
            if (this.disposeAfter) {
              this.disposed.push([oldVal, k, 'set'])
            }
          }
        }
        this.removeItemSize(index)
        this.valList[index] = v
        this.addItemSize(index, size)
      }
    }
    if (ttl !== 0 && this.ttl === 0 && !this.ttls) {
      this.initializeTTLTracking()
    }
    if (!noUpdateTTL) {
      this.setItemTTL(index, ttl, start)
    }
    if (this.disposeAfter) {
      while (this.disposed.length) {
        this.disposeAfter(...this.disposed.shift())
      }
    }
    return this
  }

  newIndex() {
    if (this.size === 0) {
      return this.tail
    }
    if (this.size === this.max && this.max !== 0) {
      return this.evict(false)
    }
    if (this.free.length !== 0) {
      return this.free.pop()
    }
    // initial fill, just keep writing down the list
    return this.initialFill++
  }

  pop() {
    if (this.size) {
      const val = this.valList[this.head]
      this.evict(true)
      return val
    }
  }

  evict(free) {
    const head = this.head
    const k = this.keyList[head]
    const v = this.valList[head]
    if (this.isBackgroundFetch(v)) {
      v.__abortController.abort()
    } else {
      this.dispose(v, k, 'evict')
      if (this.disposeAfter) {
        this.disposed.push([v, k, 'evict'])
      }
    }
    this.removeItemSize(head)
    // if we aren't about to use the index, then null these out
    if (free) {
      this.keyList[head] = null
      this.valList[head] = null
      this.free.push(head)
    }
    this.head = this.next[head]
    this.keyMap.delete(k)
    this.size--
    return head
  }

  has(k, { updateAgeOnHas = this.updateAgeOnHas } = {}) {
    const index = this.keyMap.get(k)
    if (index !== undefined) {
      if (!this.isStale(index)) {
        if (updateAgeOnHas) {
          this.updateItemAge(index)
        }
        return true
      }
    }
    return false
  }

  // like get(), but without any LRU updating or TTL expiration
  peek(k, { allowStale = this.allowStale } = {}) {
    const index = this.keyMap.get(k)
    if (index !== undefined && (allowStale || !this.isStale(index))) {
      const v = this.valList[index]
      // either stale and allowed, or forcing a refresh of non-stale value
      return this.isBackgroundFetch(v) ? v.__staleWhileFetching : v
    }
  }

  backgroundFetch(k, index, options, context) {
    const v = index === undefined ? undefined : this.valList[index]
    if (this.isBackgroundFetch(v)) {
      return v
    }
    const ac = new AC()
    const fetchOpts = {
      signal: ac.signal,
      options,
      context,
    }
    const cb = v => {
      if (!ac.signal.aborted) {
        this.set(k, v, fetchOpts.options)
      }
      return v
    }
    const eb = er => {
      if (this.valList[index] === p) {
        // if we allow stale on fetch rejections, then we need to ensure that
        // the stale value is not removed from the cache when the fetch fails.
        const noDelete =
          options.noDeleteOnFetchRejection ||
          options.allowStaleOnFetchRejection
        const del = !noDelete || p.__staleWhileFetching === undefined
        if (del) {
          this.delete(k)
        } else {
          // still replace the *promise* with the stale value,
          // since we are done with the promise at this point.
          this.valList[index] = p.__staleWhileFetching
        }
      }
      if (options.allowStaleOnFetchRejection) {
        return p.__staleWhileFetching
      } else if (p.__returned === p) {
        throw er
      }
    }
    const pcall = res => res(this.fetchMethod(k, v, fetchOpts))
    const p = new Promise(pcall).then(cb, eb)
    p.__abortController = ac
    p.__staleWhileFetching = v
    p.__returned = null
    if (index === undefined) {
      this.set(k, p, fetchOpts.options)
      index = this.keyMap.get(k)
    } else {
      this.valList[index] = p
    }
    return p
  }

  isBackgroundFetch(p) {
    return (
      p &&
      typeof p === 'object' &&
      typeof p.then === 'function' &&
      Object.prototype.hasOwnProperty.call(
        p,
        '__staleWhileFetching'
      ) &&
      Object.prototype.hasOwnProperty.call(p, '__returned') &&
      (p.__returned === p || p.__returned === null)
    )
  }

  // this takes the union of get() and set() opts, because it does both
  async fetch(
    k,
    {
      // get options
      allowStale = this.allowStale,
      updateAgeOnGet = this.updateAgeOnGet,
      noDeleteOnStaleGet = this.noDeleteOnStaleGet,
      // set options
      ttl = this.ttl,
      noDisposeOnSet = this.noDisposeOnSet,
      size = 0,
      sizeCalculation = this.sizeCalculation,
      noUpdateTTL = this.noUpdateTTL,
      // fetch exclusive options
      noDeleteOnFetchRejection = this.noDeleteOnFetchRejection,
      allowStaleOnFetchRejection = this.allowStaleOnFetchRejection,
      fetchContext = this.fetchContext,
      forceRefresh = false,
    } = {}
  ) {
    if (!this.fetchMethod) {
      return this.get(k, {
        allowStale,
        updateAgeOnGet,
        noDeleteOnStaleGet,
      })
    }

    const options = {
      allowStale,
      updateAgeOnGet,
      noDeleteOnStaleGet,
      ttl,
      noDisposeOnSet,
      size,
      sizeCalculation,
      noUpdateTTL,
      noDeleteOnFetchRejection,
      allowStaleOnFetchRejection,
    }

    let index = this.keyMap.get(k)
    if (index === undefined) {
      const p = this.backgroundFetch(k, index, options, fetchContext)
      return (p.__returned = p)
    } else {
      // in cache, maybe already fetching
      const v = this.valList[index]
      if (this.isBackgroundFetch(v)) {
        return allowStale && v.__staleWhileFetching !== undefined
          ? v.__staleWhileFetching
          : (v.__returned = v)
      }

      // if we force a refresh, that means do NOT serve the cached value,
      // unless we are already in the process of refreshing the cache.
      if (!forceRefresh && !this.isStale(index)) {
        this.moveToTail(index)
        if (updateAgeOnGet) {
          this.updateItemAge(index)
        }
        return v
      }

      // ok, it is stale or a forced refresh, and not already fetching.
      // refresh the cache.
      const p = this.backgroundFetch(k, index, options, fetchContext)
      return allowStale && p.__staleWhileFetching !== undefined
        ? p.__staleWhileFetching
        : (p.__returned = p)
    }
  }

  get(
    k,
    {
      allowStale = this.allowStale,
      updateAgeOnGet = this.updateAgeOnGet,
      noDeleteOnStaleGet = this.noDeleteOnStaleGet,
    } = {}
  ) {
    const index = this.keyMap.get(k)
    if (index !== undefined) {
      const value = this.valList[index]
      const fetching = this.isBackgroundFetch(value)
      if (this.isStale(index)) {
        // delete only if not an in-flight background fetch
        if (!fetching) {
          if (!noDeleteOnStaleGet) {
            this.delete(k)
          }
          return allowStale ? value : undefined
        } else {
          return allowStale ? value.__staleWhileFetching : undefined
        }
      } else {
        // if we're currently fetching it, we don't actually have it yet
        // it's not stale, which means this isn't a staleWhileRefetching,
        // so we just return undefined
        if (fetching) {
          return undefined
        }
        this.moveToTail(index)
        if (updateAgeOnGet) {
          this.updateItemAge(index)
        }
        return value
      }
    }
  }

  connect(p, n) {
    this.prev[n] = p
    this.next[p] = n
  }

  moveToTail(index) {
    // if tail already, nothing to do
    // if head, move head to next[index]
    // else
    //   move next[prev[index]] to next[index] (head has no prev)
    //   move prev[next[index]] to prev[index]
    // prev[index] = tail
    // next[tail] = index
    // tail = index
    if (index !== this.tail) {
      if (index === this.head) {
        this.head = this.next[index]
      } else {
        this.connect(this.prev[index], this.next[index])
      }
      this.connect(this.tail, index)
      this.tail = index
    }
  }

  get del() {
    deprecatedMethod('del', 'delete')
    return this.delete
  }

  delete(k) {
    let deleted = false
    if (this.size !== 0) {
      const index = this.keyMap.get(k)
      if (index !== undefined) {
        deleted = true
        if (this.size === 1) {
          this.clear()
        } else {
          this.removeItemSize(index)
          const v = this.valList[index]
          if (this.isBackgroundFetch(v)) {
            v.__abortController.abort()
          } else {
            this.dispose(v, k, 'delete')
            if (this.disposeAfter) {
              this.disposed.push([v, k, 'delete'])
            }
          }
          this.keyMap.delete(k)
          this.keyList[index] = null
          this.valList[index] = null
          if (index === this.tail) {
            this.tail = this.prev[index]
          } else if (index === this.head) {
            this.head = this.next[index]
          } else {
            this.next[this.prev[index]] = this.next[index]
            this.prev[this.next[index]] = this.prev[index]
          }
          this.size--
          this.free.push(index)
        }
      }
    }
    if (this.disposed) {
      while (this.disposed.length) {
        this.disposeAfter(...this.disposed.shift())
      }
    }
    return deleted
  }

  clear() {
    for (const index of this.rindexes({ allowStale: true })) {
      const v = this.valList[index]
      if (this.isBackgroundFetch(v)) {
        v.__abortController.abort()
      } else {
        const k = this.keyList[index]
        this.dispose(v, k, 'delete')
        if (this.disposeAfter) {
          this.disposed.push([v, k, 'delete'])
        }
      }
    }

    this.keyMap.clear()
    this.valList.fill(null)
    this.keyList.fill(null)
    if (this.ttls) {
      this.ttls.fill(0)
      this.starts.fill(0)
    }
    if (this.sizes) {
      this.sizes.fill(0)
    }
    this.head = 0
    this.tail = 0
    this.initialFill = 1
    this.free.length = 0
    this.calculatedSize = 0
    this.size = 0
    if (this.disposed) {
      while (this.disposed.length) {
        this.disposeAfter(...this.disposed.shift())
      }
    }
  }

  get reset() {
    deprecatedMethod('reset', 'clear')
    return this.clear
  }

  get length() {
    deprecatedProperty('length', 'size')
    return this.size
  }

  static get AbortController() {
    return AC
  }
  static get AbortSignal() {
    return AS
  }
}

module.exports = LRUCache


/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"ipywebcam","version":"0.1.6","description":"A Custom Jupyter Widget Library for Web Camera using WebRTC","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/vipcxj/ipywebcam","bugs":{"url":"https://github.com/vipcxj/ipywebcam/issues"},"license":"BSD-3-Clause","author":{"name":"Xiaojing Chen","email":"vipcxj@126.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/vipcxj/ipywebcam"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipywebcam/labextension","clean:nbextension":"rimraf ipywebcam/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6","lru-cache":"^7.16.1"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyter-widgets/base-manager":"^1.0.2","@jupyterlab/builder":"^3.0.0","@lumino/application":"^1.6.0","@lumino/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipywebcam/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/nonce */
/******/ 	(() => {
/******/ 		__webpack_require__.nc = undefined;
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module is referenced by other modules so it can't be inlined
/******/ 	var __webpack_exports__ = __webpack_require__("./src/extension.ts");
/******/ 	
/******/ 	return __webpack_exports__;
/******/ })()
;
});;
//# sourceMappingURL=index.js.map