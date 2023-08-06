(self["webpackChunkipynao"] = self["webpackChunkipynao"] || []).push([["lib_widget_js"],{

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

/***/ "./lib/qimessaging.js":
/*!****************************!*\
  !*** ./lib/qimessaging.js ***!
  \****************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.QiSession = void 0;
/*
**  Copyright (C) Aldebaran Robotics
**  See COPYING for the license
**
**  Author(s):
**   - Laurent LEC    <llec@aldebaran-robotics.com>
**
*/
const nao_socket_io_1 = __webpack_require__(/*! nao-socket.io */ "webpack/sharing/consume/default/nao-socket.io/nao-socket.io");
class QiSession {
    constructor(ipAddress = "nao.local") {
        this.connected = false;
        // console.log("DBG Emile qim about to connect w/17"); REMOVE
        let _socket = nao_socket_io_1.io.connect("nao:nao@" + ipAddress + ":80", { resource: "libs/qimessaging/2/socket.io",
            'force new connection': true });
        // console.log("DBG Emile qim connecting.."); REMOVE
        let _dfd = new Array();
        let _sigs = new Array();
        let _idm = 0;
        _socket.on('reply', function (data) {
            // console.log("DBG Emile qim reply"); REMOVE
            let idm = data["idm"];
            if (data["result"] != null && data["result"]["metaobject"] != undefined) {
                // let o = new Object();
                let o = {
                    __MetaObject: data["result"]["metaobject"],
                };
                let pyobj = data["result"]["pyobject"];
                _sigs[pyobj] = new Array();
                let methods = o.__MetaObject["methods"];
                for (let i in methods) {
                    let methodName = methods[i]["name"];
                    // @ts-ignore
                    o[methodName] = createMetaCall(pyobj, methodName, "data");
                }
                let signals = o.__MetaObject["signals"];
                for (let i in signals) {
                    let signalName = signals[i]["name"];
                    // @ts-ignore
                    o[signalName] = createMetaSignal(pyobj, signalName, false);
                }
                let properties = o.__MetaObject["properties"];
                for (let i in properties) {
                    let propertyName = properties[i]["name"];
                    // @ts-ignore
                    o[propertyName] = createMetaSignal(pyobj, propertyName, true);
                }
                _dfd[idm].resolve(o);
            }
            else {
                if (_dfd[idm].__cbi != undefined) {
                    let cbi = _dfd[idm].__cbi;
                    _sigs[cbi["obj"]][cbi["signal"]][data["result"]] = cbi["cb"];
                }
                _dfd[idm].resolve(data["result"]);
            }
            delete _dfd[idm];
        });
        _socket.on('error', function (data) {
            // console.log("DBG Emile qim error"); REMOVE
            if (data["idm"] != undefined) {
                _dfd[data["idm"]].reject(data["result"]);
                delete _dfd[data["idm"]];
            }
        });
        _socket.on('signal', function (data) {
            // console.log("DBG Emile qim signal"); REMOVE
            let res = data["result"];
            let callback = _sigs[res["obj"]][res["signal"]][res["link"]];
            if (callback != undefined) {
                // @ts-ignore
                callback.apply(this, res["data"]);
            }
        });
        _socket.on('disconnect', function (data) {
            // console.log("DBG Emile qim disconnect"); REMOVE
            for (let idm in _dfd) {
                _dfd[idm].reject("Call " + idm + " canceled: disconnected");
                delete _dfd[idm];
            }
            // @ts-ignore
            if (this.disconnected) {
                // disconnected();
                console.log("DBG Isabel disconnected");
            }
        });
        function createMetaCall(obj, member, data) {
            return function () {
                let idm = ++_idm;
                let args = Array.prototype.slice.call(arguments, 0);
                let promise = new Promise(function (resolve, reject) {
                    _dfd[idm] = { resolve: resolve, reject: reject };
                });
                if (args[0] == "connect") {
                    _dfd[idm].__cbi = data;
                }
                _socket.emit('call', { idm: idm, params: { obj: obj, member: member, args: args } });
                return promise;
            };
        }
        ;
        function createMetaSignal(obj, signal, isProperty) {
            // let s = new Object();
            let s = {};
            _sigs[obj][signal] = new Array();
            s.connect = function (cb) {
                // @ts-ignore
                return createMetaCall(obj, signal, { obj: obj, signal: signal, cb: cb })("connect");
            };
            // @ts-ignore
            s.disconnect = function (l) {
                delete _sigs[obj][signal][l];
                // @ts-ignore
                return createMetaCall(obj, signal, "data")("disconnect", l);
            };
            if (!isProperty) {
                return s;
            }
            s.setValue = function () {
                let args = Array.prototype.slice.call(arguments, 0);
                // @ts-ignore
                return createMetaCall(obj, signal, "data").apply(this, ["setValue"].concat(args));
            };
            s.value = function () {
                // @ts-ignore
                return createMetaCall(obj, signal, "data")("value");
            };
            return s;
        }
        this.service = createMetaCall("ServiceDirectory", "service", "data");
        // let _self = this;
        _socket.on('connect', function () {
            // console.log("DBG Emile qim connect"); REMOVE
            // @ts-ignore
            if (this.connected) {
                // connected(_self);
                console.log("DBG Isabel already connected");
            }
        });
        // console.log("DBG Emile qim done with init"); REMOVE
    }
}
exports.QiSession = QiSession;


/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Isabel Paredes
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

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Isabel Paredes
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
exports.NaoRobotView = exports.NaoRobotModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
const qimessaging_1 = __webpack_require__(/*! ./qimessaging */ "./lib/qimessaging.js");
class NaoRobotModel extends base_1.DOMWidgetModel {
    constructor() {
        super(...arguments);
        this.connected = "Disconnected";
        this.status = "Not busy";
    }
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: NaoRobotModel.model_name, _model_module: NaoRobotModel.model_module, _model_module_version: NaoRobotModel.model_module_version, _view_name: NaoRobotModel.view_name, _view_module: NaoRobotModel.view_module, _view_module_version: NaoRobotModel.view_module_version, value: 'Hello World', synco: "something silly", connected: "Disconnected", status: "Not busy" });
    }
    initialize(attributes, options) {
        super.initialize(attributes, options);
        this.on("msg:custom", this.onCommand);
    }
    changeStatus(statusMessage) {
        this.status = statusMessage;
        this.set("status", statusMessage);
        this.save_changes();
    }
    connect(ipAddress) {
        return __awaiter(this, void 0, void 0, function* () {
            console.log("REMOVE the command was to connect");
            this.changeStatus("Establishing connection");
            this.qiSession = new qimessaging_1.QiSession(ipAddress);
            this.connected = "Connected";
            this.set("connected", "Connected");
            this.save_changes();
            this.changeStatus("Not busy");
        });
    }
    disconnect() {
        console.log("REMOVE disconnecting");
        // TODO: Make disconnect function
        // delete this.qiSession;
        this.connected = "Disconnected";
        this.changeStatus("Unavailable");
    }
    Testing() {
        return __awaiter(this, void 0, void 0, function* () {
            this.qiSession = new qimessaging_1.QiSession();
            const tts = yield this.qiSession.service("ALTextToSpeech");
            // let msg : any = Object.getOwnPropertyNames(tts);
            let aThing = this.send(tts);
            console.log("A thing: ", aThing);
            console.log("JS sent something");
        });
    }
    goSleep(tSeconds) {
        return __awaiter(this, void 0, void 0, function* () {
            console.log("IN THE SLEEPING SESH");
            const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
            yield sleep(tSeconds * 1000);
            console.log("WAKING UP");
            this.set("synco", "something else");
            this.save_changes();
            this.send({ data: "purple" });
            console.log("SETTED THE VALUE");
        });
    }
    callService(serviceName, methodName, args, kwargs) {
        return __awaiter(this, void 0, void 0, function* () {
            const naoService = yield this.qiSession.service(serviceName);
            this.changeStatus("Running method" + methodName);
            yield naoService[methodName](...args);
            this.changeStatus("Task completed");
        });
    }
    onCommand(commandData, buffers) {
        return __awaiter(this, void 0, void 0, function* () {
            console.log("REMOVE onCommand", commandData);
            const cmd = commandData["command"];
            switch (cmd) {
                case "connect":
                    yield this.connect(commandData["ipAddress"]);
                    break;
                case "disconnect":
                    this.disconnect();
                    break;
                case "callService":
                    console.log("RECEIVING COMMAND FOR SERVICE");
                    yield this.callService(commandData["service"], commandData["method"], commandData["args"], commandData["kwargs"]);
                    break;
            }
            console.log("End of OnCommand");
        });
    }
}
exports.NaoRobotModel = NaoRobotModel;
NaoRobotModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
// var qiSession = // TODO:
NaoRobotModel.model_name = 'NaoRobotModel';
NaoRobotModel.model_module = version_1.MODULE_NAME;
NaoRobotModel.model_module_version = version_1.MODULE_VERSION;
NaoRobotModel.view_name = 'NaoRobotView'; // Set to null if no view
NaoRobotModel.view_module = version_1.MODULE_NAME; // Set to null if no view
NaoRobotModel.view_module_version = version_1.MODULE_VERSION;
class NaoRobotView extends base_1.DOMWidgetView {
    render() {
        this.el.classList.add('custom-widget');
        // Connection element
        this.txt_connected = document.createElement('div');
        this.txt_connected.textContent = "Disconnected";
        this.el.appendChild(this.txt_connected);
        // Status element
        this.txt_status = document.createElement('div');
        this.txt_status.textContent = "Not busy";
        this.el.appendChild(this.txt_status);
        // Testing element
        this.synco = document.createElement('div');
        this.synco.textContent = "it should be here";
        this.el.appendChild(this.synco);
        console.log("RENDERING");
        console.log(this.model.get("connected"), " CONNECTED");
        console.log(this.model.get("synco"), " SYNCO");
        this.value_changed();
        this.model.on('change:connected', this.value_changed, this);
        this.model.on('change:status', this.value_changed, this);
        this.model.on('change:synco', this.value_changed, this);
    }
    value_changed() {
        // this.el.textContent = this.model.get('value');
        // this.synco = this.model.get('synco');
        console.log("THE VALUE CHANGED");
        this.txt_connected.textContent = this.model.get("connected");
        this.txt_status.textContent = this.model.get("status");
        this.synco.textContent = this.model.get('synco');
    }
}
exports.NaoRobotView = NaoRobotView;


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

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"ipynao","version":"0.1.0","description":"A widget library for controlling Nao","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/QuantStack/ipynao","bugs":{"url":"https://github.com/QuantStack/ipynao/issues"},"license":"BSD-3-Clause","author":{"name":"Isabel Paredes","email":"isabel.paredes@quantstack.net"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/ihuicatl/ipynao"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack --mode=production","build:nbextension:dev":"webpack --mode=development","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipynao/labextension","clean:nbextension":"rimraf ipynao/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6","nao-socket.io":"^1.0.2"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyter-widgets/base-manager":"^1.0.2","@jupyterlab/builder":"^3.0.0","@lumino/application":"^1.6.0","@lumino/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipynao/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.9bd9861460f0e65d07d5.js.map