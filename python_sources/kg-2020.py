#!/usr/bin/env python
# coding: utf-8

# ## Introduction
# Greetings from the Kaggle bot! This is an automatically-generated kernel with starter code demonstrating how to read in the data and begin exploring. If you're inspired to dig deeper, click the blue "Fork Notebook" button at the top of this kernel to begin editing.

# ## Exploratory Analysis
# To begin this exploratory analysis, first import libraries and define functions for plotting the data using `matplotlib`. Depending on the data, not all plots will be made. (Hey, I'm just a simple kerneling bot, not a Kaggle Competitions Grandmaster!)

# In[ ]:


from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# There is 0 csv file in the current version of the dataset:
# 

# In[ ]:


for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# The next hidden code cells define functions for plotting data. Click on the "Code" button in the published kernel to reveal the hidden code.

# In[ ]:


# Distribution graphs (histogram/bar graph) of column data
def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) / nGraphPerRow
    plt.figure(num = None, figsize = (6 * nGraphPerRow, 8 * nGraphRow), dpi = 80, facecolor = 'w', edgecolor = 'k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 1.0, w_pad = 1.0, h_pad = 1.0)
    plt.show()


# In[ ]:


# Correlation matrix
def plotCorrelationMatrix(df, graphWidth):
    filename = df.dataframeName
    df = df.dropna('columns') # drop columns with NaN
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    if df.shape[1] < 2:
        print(f'No correlation plots shown: The number of non-NaN or constant columns ({df.shape[1]}) is less than 2')
        return
    corr = df.corr()
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='w', edgecolor='k')
    corrMat = plt.matshow(corr, fignum = 1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title(f'Correlation Matrix for {filename}', fontsize=15)
    plt.show()


# In[ ]:


# Scatter and density plots
def plotScatterMatrix(df, plotSize, textSize):
    df = df.select_dtypes(include =[np.number]) # keep only numerical columns
    # Remove rows and columns that would lead to df being singular
    df = df.dropna('columns')
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    columnNames = list(df)
    if len(columnNames) > 10: # reduce the number of columns for matrix inversion of kernel density plots
        columnNames = columnNames[:10]
    df = df[columnNames]
    ax = pd.plotting.scatter_matrix(df, alpha=0.75, figsize=[plotSize, plotSize], diagonal='kde')
    corrs = df.corr().values
    for i, j in zip(*plt.np.triu_indices_from(ax, k = 1)):
        ax[i, j].annotate('Corr. coef = %.3f' % corrs[i, j], (0.8, 0.2), xycoords='axes fraction', ha='center', va='center', size=textSize)
    plt.suptitle('Scatter and Density Plot')
    plt.show()


# Oh, no! There are no automatic insights available for the file types used in this dataset. As your Kaggle kerneler bot, I'll keep working to fine-tune my hyper-parameters. In the meantime, please feel free to try a different dataset.

# ## Conclusion
# This concludes your starter analysis! To go forward from here, click the blue "Fork Notebook" button at the top of this kernel. This will create a copy of the code and environment for you to edit. Delete, modify, and add code as you please. Happy Kaggling!

# In[ ]:


*.pyc
build/
dist/
colout.egg-info/
.eggs/


# In[ ]:


#!/usr/bin/env python3

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist upload')
    sys.exit()

packages = ['colout']

requires = ['argparse; python_version < "2.7"', 'pygments', 'babel']

setup_requires = ['setuptools_scm']

setup(
    name='colout',
    use_scm_version=True,
    description='Color Up Arbitrary Command Output.',
    long_description=open('README.md').read(),
    author='nojhan',
    author_email='nojhan@nojhan.net',
    url='http://nojhan.github.com/colout/',
    packages=packages,
    package_data={'': ['LICENSE', 'README.md']},
    package_dir={'colout': 'colout'},
    scripts=['bin/colout'],
    setup_requires=setup_requires,
    include_package_data=True,
    install_requires=requires,
    license='GPLv3',
    zip_safe=False,
)


# In[ ]:




**()
* The code below uses open source software. Please visit the URL below for an overview of the licenses:
* http://js.api.here.com/v3/3.1.14.0/HERE_NOTICE
*/

(function(){var n,aa=[];function ba(a){return function(){return aa[a].apply(this,arguments)}}function da(a,b){return aa[a]=b}var ea="function"==typeof Object.defineProperties?Object.defineProperty:function(a,b,c){a!=Array.prototype&&a!=Object.prototype&&(a[b]=c.value)},fa="undefined"!=typeof window&&window===this?this:"undefined"!=typeof global&&null!=global?global:this;
function ha(a,b){if(b){var c=fa;a=a.split(".");for(var d=0;d<a.length-1;d++){var e=a[d];e in c||(c[e]={});c=c[e]}a=a[a.length-1];d=c[a];b=b(d);b!=d&&null!=b&&ea(c,a,{configurable:!0,writable:!0,value:b})}}function ia(a){var b=0;return function(){return b<a.length?{done:!1,value:a[b++]}:{done:!0}}}function ja(){ja=function(){};fa.Symbol||(fa.Symbol=ka)}function la(a,b){this.a=a;ea(this,"description",{configurable:!0,writable:!0,value:b})}la.prototype.toString=function(){return this.a};
var ka=function(){function a(c){if(this instanceof a)throw new TypeError("Symbol is not a constructor");return new la("jscomp_symbol_"+(c||"")+"_"+b++,c)}var b=0;return a}();function ma(){ja();var a=fa.Symbol.iterator;a||(a=fa.Symbol.iterator=fa.Symbol("Symbol.iterator"));"function"!=typeof Array.prototype[a]&&ea(Array.prototype,a,{configurable:!0,writable:!0,value:function(){return na(ia(this))}});ma=function(){}}
function na(a){ma();a={next:a};a[fa.Symbol.iterator]=function(){return this};return a}function oa(a,b){ma();a instanceof String&&(a+="");var c=0,d={next:function(){if(c<a.length){var e=c++;return{value:b(e,a[e]),done:!1}}d.next=function(){return{done:!0,value:void 0}};return d.next()}};d[Symbol.iterator]=function(){return d};return d}ha("Array.prototype.keys",function(a){return a?a:function(){return oa(this,function(b){return b})}});var pa;
if("function"==typeof Object.setPrototypeOf)pa=Object.setPrototypeOf;else{var qa;a:{var ra={Dg:!0},sa={};try{sa.__proto__=ra;qa=sa.Dg;break a}catch(a){}qa=!1}pa=qa?function(a,b){a.__proto__=b;if(a.__proto__!==b)throw new TypeError(a+" is not extensible");return a}:null}var ta=pa;ha("Object.setPrototypeOf",function(a){return a||ta});function ua(a){var b="undefined"!=typeof Symbol&&Symbol.iterator&&a[Symbol.iterator];return b?b.call(a):{next:ia(a)}}
ha("Promise",function(a){function b(g){this.A=0;this.b=void 0;this.a=[];var h=this.c();try{g(h.resolve,h.reject)}catch(k){h.reject(k)}}function c(){this.a=null}function d(g){return g instanceof b?g:new b(function(h){h(g)})}if(a)return a;c.prototype.b=function(g){if(null==this.a){this.a=[];var h=this;this.c(function(){h.g()})}this.a.push(g)};var e=fa.setTimeout;c.prototype.c=function(g){e(g,0)};c.prototype.g=function(){for(;this.a&&this.a.length;){var g=this.a;this.a=[];for(var h=0;h<g.length;++h){var k=
g[h];g[h]=null;try{k()}catch(l){this.f(l)}}}this.a=null};c.prototype.f=function(g){this.c(function(){throw g;})};b.prototype.c=function(){function g(l){return function(m){k||(k=!0,l.call(h,m))}}var h=this,k=!1;return{resolve:g(this.o),reject:g(this.f)}};b.prototype.o=function(g){if(g===this)this.f(new TypeError("A Promise cannot resolve to itself"));else if(g instanceof b)this.v(g);else{a:switch(typeof g){case "object":var h=null!=g;break a;case "function":h=!0;break a;default:h=!1}h?this.m(g):this.g(g)}};
b.prototype.m=function(g){var h=void 0;try{h=g.then}catch(k){this.f(k);return}"function"==typeof h?this.ja(h,g):this.g(g)};b.prototype.f=function(g){this.j(2,g)};b.prototype.g=function(g){this.j(1,g)};b.prototype.j=function(g,h){if(0!=this.A)throw Error("Cannot settle("+g+", "+h+"): Promise already settled in state"+this.A);this.A=g;this.b=h;this.i()};b.prototype.i=function(){if(null!=this.a){for(var g=0;g<this.a.length;++g)f.b(this.a[g]);this.a=null}};var f=new c;b.prototype.v=function(g){var h=
this.c();g.wf(h.resolve,h.reject)};b.prototype.ja=function(g,h){var k=this.c();try{g.call(h,k.resolve,k.reject)}catch(l){k.reject(l)}};b.prototype.then=function(g,h){function k(p,r){return"function"==typeof p?function(v){try{l(p(v))}catch(w){m(w)}}:r}var l,m,q=new b(function(p,r){l=p;m=r});this.wf(k(g,l),k(h,m));return q};b.prototype.catch=function(g){return this.then(void 0,g)};b.prototype.wf=function(g,h){function k(){switch(l.A){case 1:g(l.b);break;case 2:h(l.b);break;default:throw Error("Unexpected state: "+
l.A);}}var l=this;null==this.a?f.b(k):this.a.push(k)};b.resolve=d;b.reject=function(g){return new b(function(h,k){k(g)})};b.race=function(g){return new b(function(h,k){for(var l=ua(g),m=l.next();!m.done;m=l.next())d(m.value).wf(h,k)})};b.all=function(g){var h=ua(g),k=h.next();return k.done?d([]):new b(function(l,m){function q(v){return function(w){p[v]=w;r--;0==r&&l(p)}}var p=[],r=0;do p.push(void 0),r++,d(k.value).wf(q(p.length-1),m),k=h.next();while(!k.done)})};return b});
ha("Array.prototype.fill",function(a){return a?a:function(b,c,d){var e=this.length||0;0>c&&(c=Math.max(0,e+c));if(null==d||d>e)d=e;d=Number(d);0>d&&(d=Math.max(0,e+d));for(c=Number(c||0);c<d;c++)this[c]=b;return this}});ha("Math.log2",function(a){return a?a:function(b){return Math.log(b)/Math.LN2}});var va=this||self;
function wa(a,b,c){a=a.split(".");c=c||va;a[0]in c||"undefined"==typeof c.execScript||c.execScript("var "+a[0]);for(var d;a.length&&(d=a.shift());)a.length||void 0===b?c[d]&&c[d]!==Object.prototype[d]?c=c[d]:c=c[d]={}:c[d]=b}function xa(){}
function ya(a){var b=typeof a;if("object"==b)if(a){if(a instanceof Array)return"array";if(a instanceof Object)return b;var c=Object.prototype.toString.call(a);if("[object Window]"==c)return"object";if("[object Array]"==c||"number"==typeof a.length&&"undefined"!=typeof a.splice&&"undefined"!=typeof a.propertyIsEnumerable&&!a.propertyIsEnumerable("splice"))return"array";if("[object Function]"==c||"undefined"!=typeof a.call&&"undefined"!=typeof a.propertyIsEnumerable&&!a.propertyIsEnumerable("call"))return"function"}else return"null";
else if("function"==b&&"undefined"==typeof a.call)return"object";return b}function za(a){var b=ya(a);return"array"==b||"object"==b&&"number"==typeof a.length}function Ba(a){return"function"==ya(a)}function Ca(a){var b=typeof a;return"object"==b&&null!=a||"function"==b}var Da="closure_uid_"+(1E9*Math.random()>>>0),Ea=0;function Fa(a,b,c){return a.call.apply(a.bind,arguments)}
function Ga(a,b,c){if(!a)throw Error();if(2<arguments.length){var d=Array.prototype.slice.call(arguments,2);return function(){var e=Array.prototype.slice.call(arguments);Array.prototype.unshift.apply(e,d);return a.apply(b,e)}}return function(){return a.apply(b,arguments)}}function Ha(a,b,c){Function.prototype.bind&&-1!=Function.prototype.bind.toString().indexOf("native code")?Ha=Fa:Ha=Ga;return Ha.apply(null,arguments)}
function Ia(a,b){var c=Array.prototype.slice.call(arguments,1);return function(){var d=c.slice();d.push.apply(d,arguments);return a.apply(this,d)}}function t(a,b){wa(a,b,void 0)}function u(a,b){function c(){}c.prototype=b.prototype;a.l=b.prototype;a.prototype=new c;a.prototype.constructor=a;a.Do=function(d,e,f){for(var g=Array(arguments.length-2),h=2;h<arguments.length;h++)g[h-2]=arguments[h];return b.prototype[e].apply(d,g)}};function Ja(a){if(Error.captureStackTrace)Error.captureStackTrace(this,Ja);else{var b=Error().stack;b&&(this.stack=b)}a&&(this.message=String(a))}u(Ja,Error);Ja.prototype.name="CustomError";function Ka(a,b){this.c=a;this.f=b;this.b=0;this.a=null}Ka.prototype.get=function(){if(0<this.b){this.b--;var a=this.a;this.a=a.next;a.next=null}else a=this.c();return a};Ka.prototype.put=function(a){this.f(a);100>this.b&&(this.b++,a.next=this.a,this.a=a)};function La(){this.b=this.a=null}var Na=new Ka(function(){return new Ma},function(a){a.reset()});La.prototype.add=function(a,b){var c=Na.get();c.set(a,b);this.b?this.b.next=c:this.a=c;this.b=c};La.prototype.remove=function(){var a=null;this.a&&(a=this.a,this.a=this.a.next,this.a||(this.b=null),a.next=null);return a};function Ma(){this.next=this.b=this.a=null}Ma.prototype.set=function(a,b){this.a=a;this.b=b;this.next=null};Ma.prototype.reset=function(){this.next=this.b=this.a=null};var Oa=String.prototype.trim?function(a){return a.trim()}:function(a){return/^[\s\xa0]*([\s\S]*?)[\s\xa0]*$/.exec(a)[1]};function Pa(a,b){return-1!=a.indexOf(b)}function Qa(a,b){return a<b?-1:a>b?1:0};function Ra(a,b){for(var c in a)if(b.call(void 0,a[c],c,a))return!0;return!1}function Sa(a){for(var b in a)return!1;return!0}function Ta(a){var b={},c;for(c in a)b[c]=a[c];return b}var Ua="constructor hasOwnProperty isPrototypeOf propertyIsEnumerable toLocaleString toString valueOf".split(" ");function Va(a,b){for(var c,d,e=1;e<arguments.length;e++){d=arguments[e];for(c in d)a[c]=d[c];for(var f=0;f<Ua.length;f++)c=Ua[f],Object.prototype.hasOwnProperty.call(d,c)&&(a[c]=d[c])}};var Wa;a:{var Xa=va.navigator;if(Xa){var Ya=Xa.userAgent;if(Ya){Wa=Ya;break a}}Wa=""}function Za(a){return Pa(Wa,a)};var $a=Array.prototype.indexOf?function(a,b){return Array.prototype.indexOf.call(a,b,void 0)}:function(a,b){if("string"===typeof a)return"string"!==typeof b||1!=b.length?-1:a.indexOf(b,0);for(var c=0;c<a.length;c++)if(c in a&&a[c]===b)return c;return-1};function ab(a,b){this.b=a===bb&&b||"";this.a=cb}var cb={},bb={},db=new ab(bb,"");function eb(a,b){this.b=a===fb&&b||"";this.a=gb}var gb={},fb={};function hb(){this.a="";this.b=ib}function jb(){var a=kb;if(a instanceof hb&&a.constructor===hb&&a.b===ib)return a.a;ya(a);return"type_error:SafeHtml"}var ib={};function lb(a){var b=new hb;b.a=a;return b}lb("<!DOCTYPE html>");var kb=lb("");lb("<br>");function mb(a){var b=new eb(fb,db instanceof ab&&db.constructor===ab&&db.a===cb?db.b:"type_error:Const");b instanceof eb&&b.constructor===eb&&b.a===gb?b=b.b:(ya(b),b="type_error:TrustedResourceUrl");a.src=b.toString()};function nb(a){nb[" "](a);return a}nb[" "]=xa;function ob(a,b){var c=pb;return Object.prototype.hasOwnProperty.call(c,a)?c[a]:c[a]=b(a)};var qb=Za("Opera"),rb=Za("Trident")||Za("MSIE"),tb=Za("Edge"),ub=Za("Gecko")&&!(Pa(Wa.toLowerCase(),"webkit")&&!Za("Edge"))&&!(Za("Trident")||Za("MSIE"))&&!Za("Edge"),vb=Pa(Wa.toLowerCase(),"webkit")&&!Za("Edge");function wb(){var a=va.document;return a?a.documentMode:void 0}var xb;
a:{var yb="",zb=function(){var a=Wa;if(ub)return/rv:([^\);]+)(\)|;)/.exec(a);if(tb)return/Edge\/([\d\.]+)/.exec(a);if(rb)return/\b(?:MSIE|rv)[: ]([^\);]+)(\)|;)/.exec(a);if(vb)return/WebKit\/(\S+)/.exec(a);if(qb)return/(?:Version)[ \/]?(\S+)/.exec(a)}();zb&&(yb=zb?zb[1]:"");if(rb){var Ab=wb();if(null!=Ab&&Ab>parseFloat(yb)){xb=String(Ab);break a}}xb=yb}var pb={};
function Bb(a){return ob(a,function(){for(var b=0,c=Oa(String(xb)).split("."),d=Oa(String(a)).split("."),e=Math.max(c.length,d.length),f=0;0==b&&f<e;f++){var g=c[f]||"",h=d[f]||"";do{g=/(\d*)(\D*)(.*)/.exec(g)||["","","",""];h=/(\d*)(\D*)(.*)/.exec(h)||["","","",""];if(0==g[0].length&&0==h[0].length)break;b=0==g[1].length?0:parseInt(g[1],10);var k=0==h[1].length?0:parseInt(h[1],10);b=Qa(b,k)||Qa(0==g[2].length,0==h[2].length)||Qa(g[2],h[2]);g=g[3];h=h[3]}while(0==b)}return 0<=b})}var Cb;
Cb=va.document&&rb?wb():void 0;!ub&&!rb||rb&&9<=Number(Cb)||ub&&Bb("1.9.1");rb&&Bb("9");function Db(a){var b=document;a=String(a);"application/xhtml+xml"===b.contentType&&(a=a.toLowerCase());return b.createElement(a)};function Eb(a){va.setTimeout(function(){throw a;},0)}var Fb;
function Gb(){var a=va.MessageChannel;"undefined"===typeof a&&"undefined"!==typeof window&&window.postMessage&&window.addEventListener&&!Za("Presto")&&(a=function(){var e=Db("IFRAME");e.style.display="none";mb(e);document.documentElement.appendChild(e);var f=e.contentWindow;e=f.document;e.open();e.write(jb());e.close();var g="callImmediate"+Math.random(),h="file:"==f.location.protocol?"*":f.location.protocol+"//"+f.location.host;e=Ha(function(k){if(("*"==h||k.origin==h)&&k.data==g)this.port1.onmessage()},
this);f.addEventListener("message",e,!1);this.port1={};this.port2={postMessage:function(){f.postMessage(g,h)}}});if("undefined"!==typeof a&&!Za("Trident")&&!Za("MSIE")){var b=new a,c={},d=c;b.port1.onmessage=function(){if(void 0!==c.next){c=c.next;var e=c.ij;c.ij=null;e()}};return function(e){d.next={ij:e};d=d.next;b.port2.postMessage(0)}}return"undefined"!==typeof document&&"onreadystatechange"in Db("SCRIPT")?function(e){var f=Db("SCRIPT");f.onreadystatechange=function(){f.onreadystatechange=null;
f.parentNode.removeChild(f);f=null;e();e=null};document.documentElement.appendChild(f)}:function(e){va.setTimeout(e,0)}};function Hb(a,b){Ib||Jb();Kb||(Ib(),Kb=!0);Lb.add(a,b)}var Ib;function Jb(){if(va.Promise&&va.Promise.resolve){var a=va.Promise.resolve(void 0);Ib=function(){a.then(Mb)}}else Ib=function(){var b=Mb;!Ba(va.setImmediate)||va.Window&&va.Window.prototype&&!Za("Edge")&&va.Window.prototype.setImmediate==va.setImmediate?(Fb||(Fb=Gb()),Fb(b)):va.setImmediate(b)}}var Kb=!1,Lb=new La;function Mb(){for(var a;a=Lb.remove();){try{a.a.call(a.b)}catch(b){Eb(b)}Na.put(a)}Kb=!1};function Ob(a){this.A=Pb;this.j=void 0;this.c=this.a=this.b=null;this.f=this.g=!1;if(a!=xa)try{var b=this;a.call(void 0,function(c){Qb(b,Rb,c)},function(c){Qb(b,Sb,c)})}catch(c){Qb(this,Sb,c)}}var Pb=0,Rb=2,Sb=3;function Tb(){this.next=this.c=this.b=this.f=this.a=null;this.g=!1}Tb.prototype.reset=function(){this.c=this.b=this.f=this.a=null;this.g=!1};var Ub=new Ka(function(){return new Tb},function(a){a.reset()});function Vb(a,b,c){var d=Ub.get();d.f=a;d.b=b;d.c=c;return d}
function Wb(a){if(a instanceof Ob)return a;var b=new Ob(xa);Qb(b,Rb,a);return b}function Xb(a){return new Ob(function(b,c){c(a)})}function Yb(){var a,b,c=new Ob(function(d,e){a=d;b=e});return new $b(c,a,b)}Ob.prototype.then=function(a,b,c){return ac(this,Ba(a)?a:null,Ba(b)?b:null,c)};Ob.prototype.$goog_Thenable=!0;Ob.prototype.cancel=function(a){if(this.A==Pb){var b=new bc(a);Hb(function(){cc(this,b)},this)}};
function cc(a,b){if(a.A==Pb)if(a.b){var c=a.b;if(c.a){for(var d=0,e=null,f=null,g=c.a;g&&(g.g||(d++,g.a==a&&(e=g),!(e&&1<d)));g=g.next)e||(f=g);e&&(c.A==Pb&&1==d?cc(c,b):(f?(d=f,d.next==c.c&&(c.c=d),d.next=d.next.next):dc(c),ec(c,e,Sb,b)))}a.b=null}else Qb(a,Sb,b)}function fc(a,b){a.a||a.A!=Rb&&a.A!=Sb||gc(a);a.c?a.c.next=b:a.a=b;a.c=b}
function ac(a,b,c,d){var e=Vb(null,null,null);e.a=new Ob(function(f,g){e.f=b?function(h){try{var k=b.call(d,h);f(k)}catch(l){g(l)}}:f;e.b=c?function(h){try{var k=c.call(d,h);void 0===k&&h instanceof bc?g(h):f(k)}catch(l){g(l)}}:g});e.a.b=a;fc(a,e);return e.a}Ob.prototype.m=function(a){this.A=Pb;Qb(this,Rb,a)};Ob.prototype.o=function(a){this.A=Pb;Qb(this,Sb,a)};
function Qb(a,b,c){if(a.A==Pb){a===c&&(b=Sb,c=new TypeError("Promise cannot resolve to itself"));a.A=1;a:{var d=c,e=a.m,f=a.o;if(d instanceof Ob){fc(d,Vb(e||xa,f||null,a));var g=!0}else{if(d)try{var h=!!d.$goog_Thenable}catch(l){h=!1}else h=!1;if(h)d.then(e,f,a),g=!0;else{if(Ca(d))try{var k=d.then;if(Ba(k)){hc(d,k,e,f,a);g=!0;break a}}catch(l){f.call(a,l);g=!0;break a}g=!1}}}g||(a.j=c,a.A=b,a.b=null,gc(a),b!=Sb||c instanceof bc||ic(a,c))}}
function hc(a,b,c,d,e){function f(k){h||(h=!0,d.call(e,k))}function g(k){h||(h=!0,c.call(e,k))}var h=!1;try{b.call(a,g,f)}catch(k){f(k)}}function gc(a){a.g||(a.g=!0,Hb(a.i,a))}function dc(a){var b=null;a.a&&(b=a.a,a.a=b.next,b.next=null);a.a||(a.c=null);return b}Ob.prototype.i=function(){for(var a;a=dc(this);)ec(this,a,this.A,this.j);this.g=!1};
function ec(a,b,c,d){if(c==Sb&&b.b&&!b.g)for(;a&&a.f;a=a.b)a.f=!1;if(b.a)b.a.b=null,jc(b,c,d);else try{b.g?b.f.call(b.c):jc(b,c,d)}catch(e){kc.call(null,e)}Ub.put(b)}function jc(a,b,c){b==Rb?a.f.call(a.c,c):a.b&&a.b.call(a.c,c)}function ic(a,b){a.f=!0;Hb(function(){a.f&&kc.call(null,b)})}var kc=Eb;function bc(a){Ja.call(this,a)}u(bc,Ja);bc.prototype.name="cancel";function $b(a,b,c){this.ii=a;this.resolve=b;this.reject=c};var x=this;function lc(){return Object.create(y,void 0)}var A=Ha,mc=String,nc=x.Object.freeze||function(a){return a};function oc(a){for(var b=Object.keys(a),c=b.length,d;c--;)d=a[b[c]],Ca(d)&&oc(d);return nc(a)}function pc(a){var b=ya(a);if("object"==b||"array"==b){if(Ba(a.clone))return a.clone();b="array"==b?[]:{};for(var c in a)a.hasOwnProperty(c)&&(b[c]=pc(a[c]));return b}return a}var B=self.eval("undefined"),y=self.eval("null");function qc(a,b){return mc(a).split(b!==B?b:" ")}var rc="prototype constructor hasOwnProperty isPrototypeOf propertyIsEnumerable toLocaleString toString valueOf".split(" ");
function C(a,b,c,d,e){if(!(b=a instanceof b)&&c)throw new D(c,d,sc(e)?e:a);return b}function tc(a,b){if(!0===(C(a,b)&&a.constructor===b))throw new TypeError("Illegal constructor "+uc(b));}function vc(a,b,c,d,e){if(!(b=wc(a)===b)&&c)throw new D(c,d,sc(e)?e:a);return b}function xc(a,b,c,d){return vc(a,"Array",b,c,d)}t("H.lang.isArray",xc);function sc(a){return a!==B}function yc(a){return"string"===typeof a}t("H.lang.isString",yc);var zc=parseInt,Ac=parseFloat,E=isNaN;
function Bc(a){return a===+a}t("H.lang.isNumber",Bc);t("H.lang.isInteger",Number.isInteger?Number.isInteger:function(a){return"number"===typeof a&&0===a%1});function Cc(a){return!E(+a)}function wc(a){var b=Object[rc[0]][rc[6]].call(a).match(/^\[object (\w+)\]$/);return b?b[1]:typeof a}var Dc=[];function Ec(a){0>Dc.indexOf(a)&&Dc.push(a)}Ec(Dc);
function uc(a,b,c,d){var e="",f=2>arguments.length,g;f&&(b={H:x.H},c="",d=Dc.slice());Fc(b,!0,function(h,k){try{if(g=h[k],k=Gc(h,g),!(Ca(g)&&g.window===g&&g.self===g||Ca(g)&&0<g.nodeType&&Ba(g.cloneNode))&&Ca(g)){if(g===a)return e=c+"."+k,!0;if(0>d.indexOf(g)&&(d.push(g),e=uc(a,g,c+"."+k,d)))return!0}}catch(l){}});f&&(e=e?e.substr(1).replace("."+rc[0]+".","#"):"~"+(Ba(a)?Hc(a)+"()":wc(a)));return e}
function Gc(a,b){var c=[];Fc(a,!1,function(d,e){d[e]===b&&c.push(e)});return c.sort(Ic)[0]}function Ic(a,b){return b.length-a.length}var Jc=Object[rc[0]][rc[2]];function Fc(a,b,c){var d;if(a){for(e in a)if((!b||Jc.call(a,e))&&c(a,e,!0))return;for(d=rc.length;d--;){var e=rc[d];if((!b||Jc.call(a,e))&&c(a,e,!1))break}}}function Hc(a){return(a=/^\s*function ([^\( ]+)/.exec(a))?a[1]:"anonymous"}function Kc(a,b,c){c[b]="#"+b}var Lc=!!x.__karma__;function Mc(){throw Error("unimplemented method");};function Nc(a,b){b=b||{};"status"in b&&(this.status=+b.status);"statusText"in b&&(this.statusText=b.statusText);this.ok=200<=this.status&&300>this.status;this.bodyUsed=!1;a?"string"===typeof a?this.c=a:ArrayBuffer&&(ArrayBuffer.prototype.isPrototypeOf(a)||a.buffer)?this.a=a.buffer||a:Blob.prototype.isPrototypeOf(a)&&(this.b=a):this.c=""}t("H.net.Response",Nc);Nc.prototype.type="default";Nc.prototype.type=Nc.prototype.type;Nc.prototype.status=200;Nc.prototype.status=Nc.prototype.status;
Nc.prototype.statusText="OK";Nc.prototype.statusText=Nc.prototype.statusText;function Oc(a){if(a.bodyUsed)return Xb(new TypeError("Already read"));a.bodyUsed=!0}Nc.error=function(){Nc.a||(Nc.a=new Nc(null,{status:0,statusText:""}),Nc.a.type="error");return Nc.a};Nc.error=Nc.error;
Nc.prototype.text=function(){var a=Oc(this);if(!a)if(this.c)a=Wb(this.c);else if(this.a){a=new Uint8Array(this.a);var b=a.length,c=Array(b),d;for(d=0;d<b;d++)c[d]=String.fromCharCode(a[d]);a=Wb(c.join(""))}else this.b?a=Qc(this.b):a=Xb("Unsupported response body");return a};Nc.prototype.json=function(){return this.text().then(x.JSON.parse)};Nc.prototype.blob=function(){var a,b=Oc(this);b||(this.b?a=this.b:this.a&&(a=new Blob([this.a],{type:"application/octet-stream"})));return b||Wb(a)};
Nc.prototype.arrayBuffer=function(){return this.a?Oc(this)||Wb(this.a.slice(0)):this.blob().then(Nc.b)};Nc.b=function(a){var b=new FileReader;b.readAsArrayBuffer(a);return new Ob(function(c,d){b.onload=function(){c(b.result)};b.onerror=function(){d(b.error)}})};function Qc(a){var b=new FileReader;b.readAsText(a);return new Ob(function(c,d){b.onload=function(){c(b.result)};b.onerror=function(){d(b.error)}})}!Lc&&x.Response&&x.Response.error&&(Nc=x.Response,Ec(Nc.prototype));function Rc(a,b,c){function d(){var m=A(l.a,l),q=+k.timeout||0;Sc?(Tc(l,"timeout",m),e.timeout=q):q&&(l.c=setTimeout(function(){e.abort();l.a({type:"timeout"})},q));Tc(l,"error",m);Tc(l,"load",m);e.send(k.data)}var e,f,g,h=c&&c.headers||{},k={},l=this;if(!Ba(b))throw new D(Rc,1,"function required");Va(h,Uc.headers,h);Va(k,Uc,c||{});k.headers=h;this.b=b;this.wa=e=new XMLHttpRequest;b=k.method;try{e.open(b,a,!0);for(f in h)h.hasOwnProperty(f)&&(g=h[f])&&e.setRequestHeader(f,g);e.withCredentials=!!k.withCredentials;
d()}catch(m){this.a({type:"cors"})}}t("H.net.Xhr",Rc);var Uc={method:"GET",headers:{},data:null},Vc="withCredentials"in new XMLHttpRequest,Sc="timeout"in new XMLHttpRequest;function Tc(a,b,c){Vc?a.wa.addEventListener(b,c):a.wa["on"+b]=c}function Wc(a,b,c){Vc?a.wa.removeEventListener(b,c):a.wa["on"+b]=null}Rc.prototype.abort=function(){this.wa&&(this.wa.abort(),this.wa&&this.a({type:"abort"}))};Rc.prototype.abort=Rc.prototype.abort;
Rc.prototype.a=function(a){var b=a.type;a=this.wa;var c,d;this.c&&clearTimeout(this.c);"load"===b?a instanceof XMLHttpRequest&&200!==a.status&&(c="network"):c=4===a.readyState&&0===a.status&&"error"==b?"cors":"error"!=b?b:"network";b=this.a;Wc(this,"timeout",b);Wc(this,"error",b);Wc(this,"load",b);0===a.status||c&&"network"!==c?d=Nc.error():d=new Nc(a.responseText,a);c=this.b;delete this.a;delete this.b;delete this.wa;c(d)};function Xc(a,b){var c=[];a&&c.push(uc(a));1<arguments.length&&c.push(""+b);c=Error(c.join(" "));Object.setPrototypeOf(c,Xc.prototype);return c}u(Xc,Error);t("H.lang.IllegalOperationError",Xc);Xc.prototype.name="IllegalOperationError";var Yc,$c,ad;function D(a,b,c){var d=arguments.length;b=b!==B?+b:b;if(b!==B){var e=(e=/^.*?\(([^\)]+)/.exec((""+a).replace(/(\/\*([\s\S]*?)\*\/)|(\/\/(.*)$)/gm,"")))?qc(e[1].replace(/\s+/g,""),","):[];e.forEach(Kc);e=e[b]||"#"+b}var f=a?uc(a):"";d=2<d?mc(c):"";if(e||d)f+=" (Argument "+(e||"")+(d?" "+d:"")+")";d=Error(f);Object.setPrototypeOf(d,D.prototype);return d}u(D,Error);t("H.lang.InvalidArgumentError",D);D.prototype.name="InvalidArgumentError";function bd(){if(!yc("STATIC_DB"))throw new D(this.constructor,0);this.g=x.indexedDB||x.vo||x.Jn||x.Kn;if(!this.g)throw new Xc(this.constructor,"This browser does not support IndexedDB");this.a=[];this.c=[];this.di=A(this.di,this)}var cd,dd;n=bd.prototype;n.put=function(a,b,c,d){if(!yc(a)&&!Bc(a))throw new D(this.put,0);if(!ed(b))throw new D(this.put,1);fd(this,function(e){gd(e.put(b,a),c,d)},d)};
n.get=function(a,b,c){var d;if(!yc(a)&&!Bc(a))throw new D(this.get,0);if(!Ba(b))throw new D(this.get,1);fd(this,function(e){d=e.get(a);gd(d,b,c)},c);return{cancel:function(){d&&(d.onsuccess=hd)}}};n.remove=function(a,b,c){if(!yc(a)&&!Bc(a))throw new D(this.remove,0);fd(this,function(d){gd(d["delete"](a),b,c)},c)};n.clear=function(a,b){fd(this,function(c){gd(c.clear(),a,b)},b)};n.di=function(){var a=this.b.result;a.objectStoreNames.contains("data")||a.createObjectStore("data")};
function id(a,b,c){if(a.b)a.a?(a.a.push(b),c&&a.c.push(c)):a.f?c&&c(a.f):b(a.b.result);else{a.b=a.g.open(jd+"STATIC_DB",1);a.b.onupgradeneeded=a.di;var d=a.b.onerror=function(){clearTimeout(a.j);a.f=this.error;a.c.forEach(function(e){e(a.f)});a.a=a.c=null};a.j=setTimeout(function(){d.call({error:Error("DbOpenTimeoutError")})},500);a.b.onsuccess=function(){clearTimeout(a.j);a.a?(a.a.forEach(function(e){e(this.result)},this),a.a=a.c=null):(a.b=a.f=null,a.a=[],a.c=[])};a.a.push(b);c&&a.c.push(c)}}
function fd(a,b,c){id(a,function(d){d=d.transaction(["data"],"readwrite");b(d.objectStore("data"))},c)}function gd(a,b,c){b&&(a.onsuccess=function(){b(this.result)});c&&(a.onerror=function(){c(this.error)})}function ed(a){var b=Object.prototype.toString.call(a);return"[object Blob]"===b||"[object ArrayBuffer]"===b||yc(a)||Ca(a)}function kd(){cd||(cd=new bd);return cd}t("H.util.IndexedDBStorage.getInstance",kd);var jd="H_";
function ld(){if(!sc(dd))if("file:"===window.location.protocol&&-1<navigator.userAgent.toLowerCase().indexOf("firefox")&&128<=window.location.href.length)dd=!1;else{var a=x.indexedDB||x.vo||x.Jn||x.Kn;var b=jd+"TEST_DB";try{var c=a&&a.open(b,1)}catch(d){}dd=!!c&&null===c.onupgradeneeded;c&&a.deleteDatabase&&a.deleteDatabase(b)}return dd}t("H.util.IndexedDBStorage.isSupported",ld);function md(){0!=nd&&(od[this[Da]||(this[Da]=++Ea)]=this);this.Bd=this.Bd;this.rb=this.rb}var nd=0,od={};md.prototype.Bd=!1;md.prototype.C=function(){if(!this.Bd&&(this.Bd=!0,this.u(),0!=nd)){var a=this[Da]||(this[Da]=++Ea);if(0!=nd&&this.rb&&0<this.rb.length)throw Error(this+" did not empty its onDisposeCallbacks queue. This probably means it overrode dispose() or disposeInternal() without calling the superclass' method.");delete od[a]}};
md.prototype.zb=function(a,b){this.Bd?void 0!==b?a.call(b):a():(this.rb||(this.rb=[]),this.rb.push(void 0!==b?Ha(a,b):a))};md.prototype.u=function(){if(this.rb)for(;this.rb.length;)this.rb.shift()()};function pd(a){a&&"function"==typeof a.C&&a.C()};function qd(a,b){this.type=a;this.currentTarget=this.target=b;this.f=this.a=!1;this.Jk=!0}qd.prototype.stopPropagation=function(){this.a=!0};qd.prototype.preventDefault=function(){this.f=!0;this.Jk=!1};t("H.util.Event",qd);qd.prototype.stopPropagation=qd.prototype.stopPropagation;qd.prototype.stopPropagation=qd.prototype.stopPropagation;qd.prototype.CAPTURING_PHASE=1;qd.prototype.CAPTURING_PHASE=qd.prototype.CAPTURING_PHASE;qd.prototype.AT_TARGET=2;qd.prototype.AT_TARGET=qd.prototype.AT_TARGET;qd.prototype.BUBBLING_PHASE=3;qd.prototype.BUBBLING_PHASE=qd.prototype.BUBBLING_PHASE;qd.prototype.eventPhase=0;qd.prototype.eventPhase=qd.prototype.eventPhase;function rd(a,b,c){rd.l.constructor.call(this,a,c);this.data=b}u(rd,qd);t("H.util.DataEvent",rd);function sd(a,b,c){sd.l.constructor.call(this,a,c);this.message=b}u(sd,qd);t("H.util.ErrorEvent",sd);var td=Math,ud=td.min,vd=td.max,wd=td.round,xd=td.floor,yd=td.ceil,zd=td.abs,Ad=td.log,Bd=td.sqrt,Cd=td.pow,Dd=td.exp,Ed=td.sin,Fd=td.asin,Gd=td.cos,Hd=td.tan,Id=td.atan,Jd=td.atan2,Kd=td.LN2,Ld=td.PI,Md=Ld/2,Nd=Ld/4,Od=2*Ld,Pd=3*Ld,Qd=Ld/180,Rd=180/Ld,Sd=1/0,Td=Cd(-2,53),Ud=Ud||function(a){return Ad(a)/Kd};function Vd(a,b){var c;return 0>(c=a%b)===0>b?c:c+b}function Wd(a,b,c){b-=c=c||0;a-=c;return a-xd(a/b)*b+c}t("H.math.normalize",Wd);function Xd(a,b,c){return a>c?c:a<b?b:a}
t("H.math.clamp",Xd);function Yd(a,b,c,d){d||(d=0);return b<c?a>=b-d&&a<=c+d:a>=c-d&&a<=b+d}function Zd(a,b,c,d,e,f){return Bd(Cd((a-e)*(d-f)-(b-f)*(c-e),2)/(Cd(c-e,2)+Cd(d-f,2)))}var $d={NONE:0,VERTEX:1,EDGE:2,SURFACE:3};t("H.math.CoverType",$d);
function ae(a,b,c,d,e,f){var g=c.length,h=g,k=c[0],l=0,m=0,q=0;d=d/2||0;var p=f||2;f=p*(e?0:1)+1;for(var r=p-2;1!=l&&h>f;){h-=r;var v=c[--h];p=c[--h];var w=c[h?h-r-1:(g+(h-r-1))%g];var z=c[h?h-r-2:(g+(h-r-2))%g];if(p>=a-d&&p<=a+d&&v>=b-d&&v<=b+d||z>=a-d&&z<=a+d&&w>=b-d&&w<=b+d)l=1;else if(!l&&p===a)z===a&&(v<b&&w>b||v>b&&w<b)||(k<=a&&z>a||k>=a&&z<a)&&(v>=b?++m:++q),l=Yd(b,v,w,d)&&Zd(a,b,p,v,z,w)<=d?2:0;else if(!l&&Yd(a,p,z,d)){if(p<a&&z>a||p>a&&z<a)k=v+(a-p)/(z-p)*(w-v),m+=k>b,q+=k<b;l=Yd(b,v,w,d)&&
Zd(a,b,p,v,z,w)<=d?2:0}k=p}!l&&e&&0!==q&&0!==m%2&&(l=3);return l}function be(a,b){return ae(a.x,a.y,b,0,!0)!==$d.NONE}t("H.math.isPointInsidePolygon",be);function ce(a){for(var b=a.length,c=new Float64Array(2*b),d=b&&sc(a[0].x);b--;){var e=a[b],f=b<<1;c[f]=d?e.x:e[0];c[f+1]=d?e.y:e[1]}return c}t("H.math.flatten",ce);function de(a,b,c){this.type=a;this.data=b;this.c=Yb();this.resolve=A(this.resolve,this);this.reject=A(this.reject,this);this.priority=ee;c!==B&&(this.priority=c);this.mh().add(this)}var ee=1,fe={zo:0,Co:ee,yo:2};n=de.prototype;n.then=function(a,b,c){return this.c.ii.then(a,b,c)};n.resolve=function(a){this.be=3;this.c.resolve(a)};n.reject=function(a){this.be=5;this.c.reject(a)};n.be=0;n.cancel=function(){this.c.ii.cancel();3>this.be&&(this.qe(),this.mh().remove(this),this.be=4)};function ge(a){var b;this.a={};for(b in fe)this.a[fe[b]]=[];this.og=a;this.og.addEventListener("allocatable",A(this.b,this))}t("H.util.JobManager",ge);var he=Object.keys(fe).map(function(a){return fe[a]}).sort().reverse();ge.prototype.add=function(a){C(a,de,this.add,0);this.a[a.priority].push(a);this.b()};ge.prototype.contains=function(a){return-1<this.a[a.priority].indexOf(a)};ge.prototype.remove=function(a){var b=a.priority;a=this.a[b].indexOf(a);return-1<a?(this.a[b].splice(a,1),!0):!1};
ge.prototype.b=function(){he.forEach(function(a){this.a[a]=this.a[a].filter(function(b){var c;if((c=this.og.Jg(b))!==y){var d=A(this.og.Wg,this.og,c,b);b.then(d,d);b.be=b.xj(c)?1:5}else return!0},this)},this)};function ie(a,b,c){var d=[],e=arguments.length;a&&d.push(uc(a));1<e&&(e=2<e&&xc(c)?" out of ["+c[0]+"..."+c[1]+"]":"",d.push("("+b+e+")"));d=Error(d.join(" "));Object.setPrototypeOf(d,ie.prototype);return d}u(ie,Error);t("H.lang.OutOfRangeError",ie);ie.prototype.name="OutOfRangeError";var je="closure_listenable_"+(1E6*Math.random()|0);function ke(a){return!(!a||!a[je])}var le=0;function me(a,b,c,d,e){this.listener=a;this.proxy=null;this.src=b;this.type=c;this.capture=!!d;this.Sf=e;this.key=++le;this.de=this.vf=!1}function ne(a){a.de=!0;a.listener=null;a.proxy=null;a.src=null;a.Sf=null};function oe(a){this.src=a;this.a={};this.b=0}oe.prototype.add=function(a,b,c,d,e){var f=a.toString();a=this.a[f];a||(a=this.a[f]=[],this.b++);var g=pe(a,b,d,e);-1<g?(b=a[g],c||(b.vf=!1)):(b=new me(b,this.src,f,!!d,e),b.vf=c,a.push(b));return b};oe.prototype.remove=function(a,b,c,d){a=a.toString();if(!(a in this.a))return!1;var e=this.a[a];b=pe(e,b,c,d);return-1<b?(ne(e[b]),Array.prototype.splice.call(e,b,1),0==e.length&&(delete this.a[a],this.b--),!0):!1};
function qe(a,b){var c=b.type;if(!(c in a.a))return!1;var d=a.a[c],e=$a(d,b),f;(f=0<=e)&&Array.prototype.splice.call(d,e,1);f&&(ne(b),0==a.a[c].length&&(delete a.a[c],a.b--));return f}oe.prototype.sa=function(a){a=a&&a.toString();var b=0,c;for(c in this.a)if(!a||c==a){for(var d=this.a[c],e=0;e<d.length;e++)++b,ne(d[e]);delete this.a[c];this.b--}return b};
function re(a,b){var c=void 0!==b,d=c?b.toString():"";return Ra(a.a,function(e){for(var f=0;f<e.length;++f)if(!c||e[f].type==d)return!0;return!1})}function pe(a,b,c,d){for(var e=0;e<a.length;++e){var f=a[e];if(!f.de&&f.listener==b&&f.capture==!!c&&f.Sf==d)return e}return-1};var se=!rb||9<=Number(Cb),te=rb&&!Bb("9");!vb||Bb("528");ub&&Bb("1.9b")||rb&&Bb("8")||qb&&Bb("9.5")||vb&&Bb("528");ub&&!Bb("8")||rb&&Bb("9");var ue=function(){if(!va.addEventListener||!Object.defineProperty)return!1;var a=!1,b=Object.defineProperty({},"passive",{get:function(){a=!0}});try{va.addEventListener("test",xa,b),va.removeEventListener("test",xa,b)}catch(c){}return a}();function ve(a,b){qd.call(this,a?a.type:"");this.relatedTarget=this.currentTarget=this.target=null;this.button=this.screenY=this.screenX=this.clientY=this.clientX=0;this.key="";this.metaKey=this.shiftKey=this.altKey=this.ctrlKey=!1;this.pointerId=0;this.pointerType="";this.b=null;if(a){var c=this.type=a.type,d=a.changedTouches&&a.changedTouches.length?a.changedTouches[0]:null;this.target=a.target||a.srcElement;this.currentTarget=b;if(b=a.relatedTarget){if(ub){a:{try{nb(b.nodeName);var e=!0;break a}catch(f){}e=
get_ipython().system('1}e||(b=null)}}else"mouseover"==c?b=a.fromElement:"mouseout"==c&&(b=a.toElement);this.relatedTarget=b;d?(this.clientX=void 0!==d.clientX?d.clientX:d.pageX,this.clientY=void 0!==d.clientY?d.clientY:d.pageY,this.screenX=d.screenX||0,this.screenY=d.screenY||0):(this.clientX=void 0!==a.clientX?a.clientX:a.pageX,this.clientY=void 0!==a.clientY?a.clientY:a.pageY,this.screenX=a.screenX||0,this.screenY=a.screenY||0);this.button=a.button;this.key=a.key||"";this.ctrlKey=a.ctrlKey;this.altKey=a.altKey;this.shiftKey=')
a.shiftKey;this.metaKey=a.metaKey;this.pointerId=a.pointerId||0;this.pointerType="string"===typeof a.pointerType?a.pointerType:we[a.pointerType]||"";this.b=a;a.defaultPrevented&&this.preventDefault()}}u(ve,qd);var we={2:"touch",3:"pen",4:"mouse"};ve.prototype.stopPropagation=function(){ve.l.stopPropagation.call(this);this.b.stopPropagation?this.b.stopPropagation():this.b.cancelBubble=!0};
ve.prototype.preventDefault=function(){ve.l.preventDefault.call(this);var a=this.b;if(a.preventDefault)a.preventDefault();else if(a.returnValue=!1,te)try{if(a.ctrlKey||112<=a.keyCode&&123>=a.keyCode)a.keyCode=-1}catch(b){}};var xe="closure_lm_"+(1E6*Math.random()|0),ye={},ze=0;function Ae(a,b,c,d,e){if(d&&d.once)return Be(a,b,c,d,e);if("array"==ya(b)){for(var f=0;f<b.length;f++)Ae(a,b[f],c,d,e);return null}c=Ce(c);return ke(a)?a.ja.add(String(b),c,!1,Ca(d)?!!d.capture:!!d,e):De(a,b,c,!1,d,e)}
function De(a,b,c,d,e,f){if(!b)throw Error("Invalid event type");var g=Ca(e)?!!e.capture:!!e,h=Ee(a);h||(a[xe]=h=new oe(a));c=h.add(b,c,d,g,f);if(c.proxy)return c;d=Fe();c.proxy=d;d.src=a;d.listener=c;if(a.addEventListener)ue||(e=g),void 0===e&&(e=!1),a.addEventListener(b.toString(),d,e);else if(a.attachEvent)a.attachEvent(Ge(b.toString()),d);else if(a.addListener&&a.removeListener)a.addListener(d);else throw Error("addEventListener and attachEvent are unavailable.");ze++;return c}
function Fe(){var a=Ie,b=se?function(c){return a.call(b.src,b.listener,c)}:function(c){c=a.call(b.src,b.listener,c);if(!c)return c};return b}function Be(a,b,c,d,e){if("array"==ya(b)){for(var f=0;f<b.length;f++)Be(a,b[f],c,d,e);return null}c=Ce(c);return ke(a)?a.ja.add(String(b),c,!0,Ca(d)?!!d.capture:!!d,e):De(a,b,c,!0,d,e)}
function Je(a,b,c,d,e){if("array"==ya(b)){for(var f=0;f<b.length;f++)Je(a,b[f],c,d,e);return null}d=Ca(d)?!!d.capture:!!d;c=Ce(c);if(ke(a))return a.ja.remove(String(b),c,d,e);if(!a)return!1;if(a=Ee(a))if(b=a.a[b.toString()],a=-1,b&&(a=pe(b,c,d,e)),c=-1<a?b[a]:null)return Ke(c);return!1}
function Ke(a){if("number"===typeof a||!a||a.de)return!1;var b=a.src;if(ke(b))return qe(b.ja,a);var c=a.type,d=a.proxy;b.removeEventListener?b.removeEventListener(c,d,a.capture):b.detachEvent?b.detachEvent(Ge(c),d):b.addListener&&b.removeListener&&b.removeListener(d);ze--;(c=Ee(b))?(qe(c,a),0==c.b&&(c.src=null,b[xe]=null)):ne(a);return!0}function Ge(a){return a in ye?ye[a]:ye[a]="on"+a}
function Le(a,b,c,d){var e=!0;if(a=Ee(a))if(b=a.a[b.toString()])for(b=b.concat(),a=0;a<b.length;a++){var f=b[a];f&&f.capture==c&&!f.de&&(f=Me(f,d),e=e&&!1!==f)}return e}function Me(a,b){var c=a.listener,d=a.Sf||a.src;a.vf&&Ke(a);return c.call(d,b)}
function Ie(a,b){if(a.de)return!0;if(!se){if(!b)a:{b=["window","event"];for(var c=va,d=0;d<b.length;d++)if(c=c[b[d]],null==c){b=null;break a}b=c}d=b;b=new ve(d,this);c=!0;if(!(0>d.keyCode||void 0!=d.returnValue)){a:{var e=!1;if(0==d.keyCode)try{d.keyCode=-1;break a}catch(g){e=!0}if(e||void 0==d.returnValue)d.returnValue=!0}d=[];for(e=b.currentTarget;e;e=e.parentNode)d.push(e);a=a.type;for(e=d.length-1;!b.a&&0<=e;e--){b.currentTarget=d[e];var f=Le(d[e],a,!0,b);c=c&&f}for(e=0;!b.a&&e<d.length;e++)b.currentTarget=
d[e],f=Le(d[e],a,!1,b),c=c&&f}return c}return Me(a,new ve(b,this))}function Ee(a){a=a[xe];return a instanceof oe?a:null}var Ne="__closure_events_fn_"+(1E9*Math.random()>>>0);function Ce(a){if(Ba(a))return a;a[Ne]||(a[Ne]=function(b){return a.handleEvent(b)});return a[Ne]};function F(){md.call(this);this.ja=new oe(this);this.rn=this;this.Yg=null}u(F,md);F.prototype[je]=!0;n=F.prototype;n.jc=function(){return this.Yg};n.ha=function(a){this.Yg=a};n.addEventListener=function(a,b,c,d){Ae(this,a,b,c,d)};n.removeEventListener=function(a,b,c,d){Je(this,a,b,c,d)};
n.dispatchEvent=function(a){var b,c=this.jc();if(c)for(b=[];c;c=c.jc())b.push(c);c=this.rn;var d=a.type||a;if("string"===typeof a)a=new qd(a,c);else if(a instanceof qd)a.target=a.target||c;else{var e=a;a=new qd(d,c);Va(a,e)}e=!0;if(b)for(var f=b.length-1;!a.a&&0<=f;f--){var g=a.currentTarget=b[f];e=g.kd(d,!0,a)&&e}a.a||(g=a.currentTarget=c,e=g.kd(d,!0,a)&&e,a.a||(e=g.kd(d,!1,a)&&e));if(b)for(f=0;!a.a&&f<b.length;f++)g=a.currentTarget=b[f],e=g.kd(d,!1,a)&&e;return e};
n.u=function(){F.l.u.call(this);this.ja&&this.ja.sa(void 0);this.Yg=null};n.kd=function(a,b,c){a=this.ja.a[String(a)];if(!a)return!0;a=a.concat();for(var d=!0,e=0;e<a.length;++e){var f=a[e];if(f&&!f.de&&f.capture==b){var g=f.listener,h=f.Sf||f.src;f.vf&&qe(this.ja,f);d=!1!==g.call(h,c)&&d}}return d&&0!=c.Jk};t("H.util.EventTarget",F);F.prototype.ha=F.prototype.ha;F.prototype.setParentEventTarget=F.prototype.ha;F.prototype.jc=F.prototype.jc;F.prototype.getParentEventTarget=F.prototype.jc;F.prototype.addEventListener=F.prototype.addEventListener;F.prototype.addEventListener=F.prototype.addEventListener;F.prototype.removeEventListener=F.prototype.removeEventListener;F.prototype.removeEventListener=F.prototype.removeEventListener;F.prototype.dispatchEvent=F.prototype.dispatchEvent;
F.prototype.dispatchEvent=F.prototype.dispatchEvent;F.prototype.C=F.prototype.C;F.prototype.dispose=F.prototype.C;F.prototype.zb=F.prototype.zb;F.prototype.addOnDisposeCallback=F.prototype.zb;F.prototype.sn=F.prototype.kd;
F.prototype.kd=function(a,b,c){var d,e,f=!0;var g=c[c.currentTarget===c.target?"AT_TARGET":b?"CAPTURING_PHASE":(d=!0,"BUBBLING_PHASE")];if(!d||"pointerenter"!==(e=c.type)&&"pointerleave"!==e)c.eventPhase=g,f=F.prototype.sn.apply(this,arguments),d&&this.jc&&null===this.jc()&&delete c.eventPhase;return f};function Oe(a){a=a||{};var b=a.callback;this.a=a.label;Ba(b)&&(this.callback=b);this.b=!!a.disabled;Oe.l.constructor.call(this)}u(Oe,F);t("H.util.ContextItem",Oe);Oe.prototype.Ge=function(){return this.a};Oe.prototype.getLabel=Oe.prototype.Ge;Oe.prototype.Nc=function(a){this.a!==a&&(this.a=a,this.dispatchEvent("update"));return this};Oe.prototype.setLabel=Oe.prototype.Nc;Oe.prototype.mc=function(){return this.b};Oe.prototype.isDisabled=Oe.prototype.mc;
Oe.prototype.Ea=function(a){a^this.b&&(this.b=a,this.dispatchEvent("update"));return this};Oe.prototype.setDisabled=Oe.prototype.Ea;var Pe=new Oe;Oe.SEPARATOR=Pe;function Qe(){if(x.document){var a=document.createElement("canvas");a.width=a.height=1;return a.getContext("2d")}return null}function Re(){return window.devicePixelRatio||1}t("H.util.getPixelRatio",Re);var Se=/^rgba\(([^,]+),([^,]+),([^,]+),([^)]+)\)$/;
function Te(a){var b=Ue[a],c=x.RegExp;b||(x.Uint8ClampedArray||(x.Uint8ClampedArray=function(d){return d instanceof Number?Array(d):d.map(function(e){return Xd(wd(e),0,255)})}),"none"===a?b=new Uint8ClampedArray([0,0,0,0]):(Ve.fillStyle="black",Ve.fillStyle=a,Se.test(Ve.fillStyle)?b=new Uint8ClampedArray([c.$1,c.$2,c.$3,255*c.$4]):(Ve.clearRect(0,0,1,1),Ve.fillRect(0,0,1,1),b=Ve.getImageData(0,0,1,1).data)),Ue[a]=b);return b}function We(a){return"none"!==a&&0<Te(a)[3]}var Ue=lc(),Xe=!!x.VBArray;
t("H.util.eval",function(a){return eval(a)});function Ye(a,b){return a!==B?a:b}function Ze(a){return/^<svg/.test(a)?"data:image/svg+xml;charset=utf-8,"+encodeURIComponent(a):a}t("H.util.provide",function(a){var b=va.$jscomp;if(b&&("function"!=typeof b.dm?0:b.dm()))throw Error("goog.provide cannot be used within a module.");wa(a,void 0)});function $e(a){this.oc=0<a?td.round(a):0}$e.prototype.next=function(a){if(9007199254740992===this.oc)throw new ie(a,this.oc,[0,9007199254740991]);return this.oc++};
var af=new $e,bf=A(af.next,af);function cf(){return!0}function df(){return!1}function hd(){}var ef=nc([]),ff=nc({});function gf(a){return"CANVAS"===a.tagName?[a]:a.getElementsByTagName("CANVAS")}function hf(a,b,c){var d;b=a.ownerDocument===b?a.cloneNode(!0):b.importNode(a,!0);if(c)for(a=gf(a),c=gf(b),d=c.length;d--;)c[d].getContext("2d").drawImage(a[d],0,0);return b}var Ve=Qe(),jf=Qe();
function kf(a){var b=a.complete,c=0<a.naturalWidth;if(b&&!c&&Xe)try{jf.drawImage(a,0,0),c=!0}catch(d){}return b&&c}var lf=x.BlobBuilder||x.WebKitBlobBuilder||x.MozBlobBuilder;function mf(a,b){b=b||"";if(lf){var c=new lf;c.append(a);a=c.getBlob(b)}else a=new Blob([a],{type:b});return a}var nf=x.navigator;$c=/Edge\/\d+/.test(nf.appVersion);ad=/(A|a)ndroid/.test(nf.appVersion);function of(){var a=of.a;a||(a=this,of.a=a,Ec(of.a),F.call(a),pf(this));return a}u(of,F);of.prototype.u=function(){of.l.u.call(this);pf(this)};function pf(a){a.g=10;a.j=6;a.a=lc();a.b=lc();a.c=0}of.prototype.Jg=function(a){a=a.type;var b=this.a[a]||0;if(this.c<this.g&&b<this.j){var c=++this.f;this.c++;this.a[a]=b+1;this.b[c+""]=a;return c}return y};
of.prototype.Wg=function(a){var b=this.b[a];if(!sc(b)||!this.a[b])throw new Xc(this.Wg,"Unknown requestId");this.c--;this.a[b]--;this.a[b]||delete this.a[b];delete this.b[a];this.dispatchEvent("allocatable")};of.prototype.f=-1;function qf(a,b,c,d){if(!this.b[a])throw new D(qf,0,"Mime type is not supported");this.g=a;a=d?Ta(d):{};"crossOrigin"in a||(a.crossOrigin="anonymous");this.a=a;rf.href=b.toString();de.call(this,rf.protocol+"//"+rf.hostname,b,c)}u(qf,de);qf.prototype.xj=function(){this.f=this.b[this.g].call(this);return!0};qf.prototype.qe=function(){this.f&&(this.f.abort(),this.f=null)};
qf.prototype.b={"application/json":function(){var a=this,b=sf(this.a),c=b.headers;b.headers=c=c?Ta(c):{};c.Accept="application/json";return new Rc(this.data,function(d){200<=d.status&&300>d.status?a.resolve(d.json()):a.reject(d)},b)},"text/plain":function(){var a=this;return new Rc(this.data,function(b){200<=b.status&&300>b.status?a.resolve(b.text()):a.reject(b)},sf(this.a))},image:function(){var a=x.document.createElement("img"),b=this,c=this.data;a.onload=A(this.resolve,this,a);a.onerror=function(){b.reject(Nc.error())};
a.crossOrigin=this.a.crossOrigin;a.src=c;return{abort:function(){a.onerror=a.onload=null;Xe&&kf(a)||a.removeAttribute("src")}}}};
(function(){try{var a=new XMLHttpRequest;a.open("get","/",!0)}catch(b){a={}}"response"in a&&(qf.prototype.b.arraybuffer=function(){var b=new XMLHttpRequest,c=this,d=this.a,e=d.headers,f;b.open("GET",this.data);tf(b,d);b.responseType="arraybuffer";if(e)for(f in e)b.setRequestHeader(f,e[f]);b.onerror=b.ontimeout=function(){c.reject(Nc.error())};b.onload=function(){c.resolve(new Nc(b.response))};b.send();return b})})();var uf=new ge(new of);qf.prototype.mh=function(){return uf};var rf=x.document.createElement("a");
function sf(a){var b=Ta(a);delete b.crossOrigin;tf(b,a);return b}function tf(a,b){a.withCredentials="use-credentials"===b.crossOrigin};function H(a,b){this.x=+a;this.y=+b}t("H.math.Point",H);H.prototype.set=H;H.prototype.set=H.prototype.set;H.prototype.clone=function(a){a?(a.x=this.x,a.y=this.y):a=new H(this.x,this.y);return a};H.prototype.clone=H.prototype.clone;H.prototype.add=function(a){this.x+=a.x;this.y+=a.y;return this};H.prototype.add=H.prototype.add;H.prototype.sub=function(a){this.x-=a.x;this.y-=a.y;return this};H.prototype.sub=H.prototype.sub;H.prototype.scale=function(a,b){this.x*=a;this.y*=void 0===b?a:b;return this};
H.prototype.scale=H.prototype.scale;H.prototype.round=function(){this.x=wd(this.x);this.y=wd(this.y);return this};H.prototype.round=H.prototype.round;H.prototype.floor=function(){this.x=xd(this.x);this.y=xd(this.y);return this};H.prototype.floor=H.prototype.floor;H.prototype.ceil=function(){this.x=yd(this.x);this.y=yd(this.y);return this};H.prototype.ceil=H.prototype.ceil;H.prototype.na=function(a){return!(!a||this.x!==a.x||this.y!==a.y)};H.prototype.equals=H.prototype.na;
H.prototype.Dj=function(a,b){var c=b.x-a.x,d=b.y-a.y,e=a;if(c||d){var f=((this.x-a.x)*c+(this.y-a.y)*d)/(c*c+d*d);0>=f?e=a:1<=f?e=b:e=new H(a.x+f*c,a.y+f*d)}return e};H.prototype.getNearest=H.prototype.Dj;H.prototype.bb=function(a){return Bd(Cd(this.x-a.x,2)+Cd(this.y-a.y,2))};H.prototype.distance=H.prototype.bb;function vf(a){if(!a)throw Error("invalid argument");return a instanceof H?a:new H(a.x,a.y)}H.fromIPoint=vf;function wf(a){var b=xf[a];if(!b)if(a in yf)b=xf[a]=a;else{b=zf.length;var c="",d=a.charAt(0).toUpperCase()+a.substr(1),e="",f=!1;Af&&(e=Af+d,f=e in yf);for(;b--&&!f;)c=zf[b],e=c+d,f=e in yf;f&&(Af=c);if(b=f?e:null)xf[a]=b;else throw Error("Could not find any variant of CSS property ["+a+"]");}return b}t("H.dom.cssPrefixer.prefix",wf);var zf=["O","Ms","ms","Moz","Webkit"],xf={},Af="",yf=document.createElement("span").style;function Bf(a,b,c,d){if(!a||!b||!c)throw new D(Bf,null,"Must specify name, version and revision parameter");this.name=a;this.version=b;this.revision=c;d&&Va(this,d)}t("H.util.BuildInfo",Bf);Bf.prototype.toString=function(){var a,b=[];for(a in this)yc(this[a])&&b.push(this[a]);return b.join(";")};var Cf={};function Df(a,b,c,d){if(!a)throw new D(Df,1,"Must specify a name parameter");return Cf[a]||(Cf[a]=new Bf(a,b,c,d))}Bf.get=Df;function Ef(){Ef.l.constructor.call(this);this.a=Ff(this);this.f=lc();this.c=A(this.c,this);this.a.addEventListener("message",this.c);this.b={}}u(Ef,F);Ef.prototype.u=function(){this.a.terminate()};Ef.prototype.j=function(a){var b=a.type,c=!!this.f[b],d=a.data,e=Gf++,f=d&&d.to?d.to:B,g=!0;c?(this.b[e]=a,Hf(this,b,e,d&&d.message,f)):(a.reject(new D(this.j,0,"processor_not_found")),g=!1);return g};
Ef.prototype.c=function(a){a=a.data;var b=this.b[a.taskId],c=a.taskId,d=a.data,e=this;if(2===a.type)(new qf("arraybuffer",d)).then(function(f){return f.arrayBuffer()}).then(function(f){e.a.postMessage(["3",c,[f]],[f])},function(){e.a.postMessage(["3",c,[null,"ERROR"]])});else{if(b){switch(a.type){case 1:b.resolve(d);break;case 0:b.reject(d)}delete this.b[c]}this.dispatchEvent(new qd(this.g.IDLE))}};var Gf=0;function If(a,b,c){var d=Gf++,e;a.b[d]=e=Yb();Hf(a,b,d,c);return e.ii}
function Hf(a,b,c,d,e){d===B||za(d)||(d=[d]);try{a.a.postMessage([b,c,d],e)}catch(f){a=a.b[c],a.reject(f.message)}}Ef.prototype.g={IDLE:"idle",Vi:"error"};Ef.prototype.i=function(a,b){var c=this.m||(this.m=new qd(this.g.Vi));c.data=b;delete this.f[a];this.dispatchEvent(c)};
function Ff(a){var b=x.H.__bootstrap__;b=Ba(b)?(""+b).replace(/^[^{]+{((.|[\r\n])+?)}\s*$/,"$1"):""+b;if(x.Worker&&x.URL)try{var c=new x.Worker(x.URL.createObjectURL(mf(b,"application/javascript")))}catch(d){}c||(a=new Jf(a),function(){eval("var self = arguments[0];"+b)}(a),c=new Kf(a));return c}function Kf(a){F.call(this);this.a=a}u(Kf,F);Kf.prototype.postMessage=function(a){x.setTimeout(A(this.b,this,a),0)};Kf.prototype.b=function(a){var b=new qd("message");b.data=a;this.a.dispatchEvent(b)};
Kf.prototype.terminate=function(){this.a.C();this.C()};function Jf(a){F.call(this);this.a=a;this.addEventListener=A(this.addEventListener,this);this.removeEventListener=A(this.removeEventListener,this);this.postMessage=A(this.postMessage,this);this.eval=A(eval,this)}u(Jf,F);Jf.prototype.postMessage=function(a){var b=new qd("message");b.data=a;x.setTimeout(A(this.a.c,this.a,b),0)};function Lf(){var a=Mf;a||(a=Mf=this,F.call(a),Nf(this));return a}var Mf;u(Lf,F);Lf.prototype.u=function(){Lf.l.u.call(this);Nf(this)};function Nf(a){var b=a.b,c;if(b)for(c=b.length;c--;)b[c].C();a.b=[];Ec(a.b);a.c=lc();a.f=lc()}
Lf.prototype.Jg=function(a){var b;a=a.type;if(b=this.f[a]){var c=this.b;var d=c[0];d||(d=c[0]=new Ef,this.zb(Ia(pd,d)),Sa(this.c)||(c=x.Object.keys(this.c),If(d,"0",c)));c=d;c.f[a]||(c.f[a]=b,If(c,"1",[a,Ba(b)?b+"":b]).then(hd,A(c.i,c,a)))}else throw new Xc(this.Jg,'Unknown type "'+a+'"');return d};Lf.prototype.Wg=function(){};Lf.prototype.a=function(a,b){var c=this.f,d=c[a];if(d){if(b!==d)throw new Xc(this.a,'Type "'+a+'" is already registered');}else c[a]=b};function Pf(a,b,c){de.call(this,a,b,c)}var Qf;u(Pf,de);Pf.prototype.mh=function(){Qf||(Qf=new ge(new Lf));return Qf};Pf.prototype.qe=function(){};Pf.prototype.xj=function(a){return a.j(this)};function Rf(a,b,c){var d=Xd(+a,-90,90);if(b&&E(d))throw new D(b,c,a);return d}function Sf(a,b,c){var d=+a;if(-180>d||180<d)d=Vd(d+180,360)-180;if(b&&E(d))throw new D(b,c,a);return d}function Tf(a,b,c){var d;if(a!==B&&E(d=+a)&&b)throw new D(b,c,a);return d}function Uf(a,b){return 0!==(0>a^0>b)&&180<zd(b-a)}t("H.geo.isDBC",Uf);function Vf(){tc(this,Vf)}t("H.geo.AbstractGeometry",Vf);Vf.prototype.getBoundingBox=Vf.prototype.G;Vf.prototype.equals=Vf.prototype.na;Vf.prototype.qb="";Vf.prototype.Ob="";Vf.prototype.toString=function(){return this.Qc([this.qb.toUpperCase()," "]).join("")};Vf.prototype.toString=Vf.prototype.toString;Vf.prototype.Pc=function(){return{type:this.Ob,coordinates:this.ed()}};Vf.prototype.toGeoJSON=Vf.prototype.Pc;Vf.prototype.V=function(){return{type:this.qb,coordinates:this.wc(),boundingBox:this.G().V()}};
Vf.prototype.forWorkerMessage=Vf.prototype.V;function Wf(a,b,c){this.lat=Rf(a,Wf,0);this.lng=Sf(b,Wf,1);c!==B&&(this.alt=Tf(c,Wf,2))}u(Wf,Vf);t("H.geo.Point",Wf);Wf.prototype.na=function(a){return this===a||!!a&&this.lat===a.lat&&this.lng===a.lng&&(this.alt||0)===(a.alt||0)};Wf.prototype.equals=Wf.prototype.na;Wf.prototype.bb=function(a){if(this===a||this.lat===a.lat&&this.lng===a.lng)a=0;else{var b=this.lat*Qd;var c=a.lat*Qd;a=1.274200158E7*Fd(ud(1,Bd(Cd(Ed((b-c)/2),2)+Gd(b)*Gd(c)*Cd(Ed((this.lng*Qd-a.lng*Qd)/2),2))))}return a};
Wf.prototype.distance=Wf.prototype.bb;
Wf.prototype.xg=function(a,b,c){if(c){if(b/=6371000.79){a*=Qd;var d=Qd*this.lat;var e=Ed(d);var f=Ed(b);var g=Gd(b);var h=Qd*this.lng;var k=Gd(d);d=Fd(k*Gd(a)*f+e*g);a=Jd(Ed(a)*k*f,g-e*Ed(d));a=(h+a+Ld)%(2*Ld)-Ld;k=a*Rd}return b?new Wf(d*Rd,(k+540)%360-180):this}a=(a%360+360)%360;if(0===(a+90)%180)return d=this.lng+b/(6371000.79*Od*Gd(this.lat*Qd))*(270===a?-360:360),new Wf(this.lat,(d+540)%360-180);if(b/=6371000.79){a*=Qd;h=this.lat*Qd;e=this.lng*Qd;f=h+b*Gd(a);g=f-h;d=Ad(Hd(f/2+Nd)/Hd(h/2+Nd));
d=E(g/d)?Gd(h):g/d;var l=b*Ed(a)/d;zd(f)>Md&&(f=0<f?Ld-f:-(Ld+f))}return b?new Wf(f*Rd,((e+l+Pd+(zd(h+g)>Md?Ld:0))%Od-Ld)*Rd):this};Wf.prototype.walk=Wf.prototype.xg;Wf.prototype.G=function(){return new J(this.lat,this.lng,this.lat,this.lng)};Wf.prototype.getBoundingBox=Wf.prototype.G;function Xf(a,b,c){var d=Ca(a)&&!(E(a.lat=Rf(a.lat))||E(a.lng=Sf(a.lng))||a.alt!==B&&E(a.alt=Tf(a.alt)));if(!d&&b)throw new D(b,c,a);return d}Wf.validate=Xf;
function Yf(a){if(!a)throw new D(Yf,0,a);return new Wf(a.lat,a.lng,a.alt)}Wf.fromIPoint=Yf;n=Wf.prototype;n.qb="Point";n.Qc=function(a){a.push("(",this.lng," ",this.lat,")");return a};n.Ob="Point";n.ed=function(){return[this.lng,this.lat,this.alt||0]};n.wc=function(){return[this.lat,this.lng,this.alt||0]};function J(a,b,c,d){Zf(this,Rf(a,J,0),Sf(b,J,1),Rf(c,J,2),Sf(d,J,3))}u(J,Vf);t("H.geo.Rect",J);J.prototype.qb="Polygon";J.prototype.Qc=function(a){var b=this.ia,c=this.aa,d=this.ma,e=this.da;a.push("(","(",c," ",b,",",e," ",b,",",e," ",d,",",c," ",d,",",c," ",b,")",")");return a};J.prototype.na=function(a){return this===a||!!a&&this.ia===a.ia&&this.aa===a.aa&&this.ma===a.ma&&this.da===a.da};J.prototype.equals=J.prototype.na;J.prototype.clone=function(){return new J(this.ia,this.aa,this.ma,this.da)};
J.prototype.clone=J.prototype.clone;function Zf(a,b,c,d,e){a.aa=c;a.da=e;b<d&&(c=b,b=d,d=c);a.ia=b;a.ma=d;a.c=a.a=a.b=null;return a}J.prototype.Tb=function(){this.c||(this.c=new Wf(this.ia,this.aa));return this.c};J.prototype.getTopLeft=J.prototype.Tb;J.prototype.Qb=function(){this.a||(this.a=new Wf(this.ma,this.da));return this.a};J.prototype.getBottomRight=J.prototype.Qb;J.prototype.Zm=function(){return this.ia};J.prototype.getTop=J.prototype.Zm;J.prototype.Zl=function(){return this.ma};
J.prototype.getBottom=J.prototype.Zl;J.prototype.zm=function(){return this.aa};J.prototype.getLeft=J.prototype.zm;J.prototype.Tm=function(){return this.da};J.prototype.getRight=J.prototype.Tm;J.prototype.ob=function(){this.b||(this.b=new Wf(this.ma+(this.ia-this.ma)/2,$f(this.aa,this.Gb())));return this.b};J.prototype.getCenter=J.prototype.ob;J.prototype.Gb=function(){return ag(this.aa,this.da)};J.prototype.getWidth=J.prototype.Gb;J.prototype.Qd=function(){return this.ia-this.ma};
J.prototype.getHeight=J.prototype.Qd;J.prototype.Hb=function(){return this.aa>this.da};J.prototype.isCDB=J.prototype.Hb;J.prototype.Vf=function(){return!this.Gb()&&!this.Qd()};J.prototype.isEmpty=J.prototype.Vf;J.prototype.G=function(){return new J(this.ia,this.aa,this.ma,this.da)};J.prototype.getBoundingBox=J.prototype.G;
J.prototype.Af=function(a,b,c){var d=this.ob();c||(a=Rf(a,this.Af,0),b=Sf(b,this.Af,1));b=this.ad(a,b,c);a=b.ob();return a.lat===d.lat&&a.lng===d.lng&&this.Qd()===b.Qd()&&this.Gb()===b.Gb()};J.prototype.containsLatLng=J.prototype.Af;J.prototype.Hd=function(a,b){b||Xf(a,this.Hd,0);return this.Af(a.lat,a.lng,b)};J.prototype.containsPoint=J.prototype.Hd;
J.prototype.Qg=function(a,b){var c=this.ob();if(!b&&!C(a,J))throw new D(this.Qg,0,a);b=this.nc(a,b);a=b.ob();return a.lat===c.lat&&a.lng===c.lng&&this.Qd()===b.Qd()&&this.Gb()===b.Gb()};J.prototype.containsRect=J.prototype.Qg;J.prototype.ad=function(a,b,c,d){if(!c){if(E(a=Rf(a)))throw new D(this.ad,0,a);if(E(b=Sf(b)))throw new D(this.ad,1,b);}return bg(this.ia,this.aa,this.ma,this.da,a,b,a,b,d)};J.prototype.mergeLatLng=J.prototype.ad;
J.prototype.mk=function(a,b,c){b||Xf(a,this.mk,0);return this.ad(a.lat,a.lng,b,c)};J.prototype.mergePoint=J.prototype.mk;J.prototype.nc=function(a,b,c){if(!b&&!C(a,J))throw new D(this.nc,0,a);return bg(this.ia,this.aa,this.ma,this.da,a.ia,a.aa,a.ma,a.da,c)};J.prototype.mergeRect=J.prototype.nc;J.prototype.Fc=function(a,b,c,d,e,f){e||(a=Rf(a,this.Fc,0),b=Sf(b,this.Fc,1),c=Rf(c,this.Fc,2),d=Sf(d,this.Fc,3));return bg(this.ia,this.aa,this.ma,this.da,a,b,c,d,f)};J.prototype.mergeTopLeftBottomRight=J.prototype.Fc;
J.prototype.qd=function(a,b){var c=this.aa<=this.da,d=a.aa<=a.da,e=this.aa<a.da,f=a.aa<this.da;if(!b&&!C(a,J))throw new D(this.qd,0,a);return this.ma<=a.ia&&a.ma<=this.ia&&(!c&&(!d||e||f)||!d&&(e||f)||e&&f)};J.prototype.intersects=J.prototype.qd;function ag(a,b){a=b-a;return a+(0>a?360:0)}function $f(a,b){a+=b/2;return a-(180<a?360:0)}
function bg(a,b,c,d,e,f,g,h,k){c=ud(c,g);a=vd(a,e);e=ag(b,d);var l=$f(b,e);g=ag(f,h);var m=$f(f,g)-l;m+=0>m-1E-6?360:0;if(180>m-1E-6){l=b;var q=h}else m=360-m,l=f,q=d;m=m+e/2+g/2;360<=m+5E-7?(l=-180,q=180):m-5E-7<e?(l=b,q=d):m-5E-7<g&&(l=f,q=h);return k?Zf(k,a,l,c,q):new J(a,l,c,q)}J.merge=bg;function cg(a,b,c){c||(Xf(a,cg,0),Xf(b,cg,1));return new J(a.lat,a.lng,b.lat,b.lng)}J.fromPoints=cg;
function dg(a,b){var c=1,d=a.length,e=null;if(!za(a))throw new D(dg,0,a);if(0<d){var f=a[0];for(e=cg(f,f,b);c<d;c++)f=a[c],e.ad(f.lat,f.lng,b,e)}return e}J.coverPoints=dg;function eg(a,b){var c=3,d=a.length,e;if(!(b||a&&null!=a.length))throw new D(eg,0,a);if(0<d)for(e=new J(a[0],a[1],a[0],a[1]);c<d;c+=3)e.ad(a[c],a[c+1],b,e);return e}J.coverLatLngAlts=eg;
function fg(a,b){var c=1,d=a.length,e;if(b&&(!a||null==a.length))throw new D(fg,0,a);if(0<d)for(e=new J(a[0].ia,a[0].aa,a[0].ma,a[0].da);c<d;c++)e.nc(a[c],b,e);return e}J.coverRects=fg;
J.prototype.Ik=function(a,b){var c=this.aa,d=this.ia,e=this.da,f=this.ma,g=this.ob().lng;Xf(a,this.Ik,0);var h=a.lat-f-(d-f)/2;var k=a.lng-g;k=180<k||-180>k?-(g+a.lng):k;a=c+(0>k?2*k:0);a=-180>a?360+a:a;e+=0<k?2*k:0;e=180<e?e-360:e;d=0<h?d+2*h:d;90<=d&&(d=90);f=0>h?f+2*h:f;-90>=f&&(f=-90);return b?Zf(b,d,a,f,e):new J(d,a,f,e)};J.prototype.resizeToCenter=J.prototype.Ik;J.prototype.Ob="Polygon";
J.prototype.ed=function(){return[[this.aa,this.ia,0],[this.da,this.ia,0],[this.da,this.ma,0],[this.aa,this.ma,0],[this.aa,this.ia,0]]};J.prototype.V=function(){return this.wc()};J.prototype.wc=function(){return[this.ia,this.aa,this.ma,this.da]};function gg(a,b,c,d,e,f){tc(this,gg);this.c=a||10;this.b=this.a=null;this.f=d||0;this.g=e||0;this.j=b||1;this.i=c||1;this.o=!!f;this.flush()}function hg(a){var b=a.b;if(a.o&&!b){var c=a.head;if(c.entries||c[0]||c[1]||c[2]||c[3])b=[c],b=ig([b,b,b,b],[c[6],c[7],c[4],c[5]]),a.b=b}return b}
function ig(a,b){var c,d,e,f,g=0;for(c=3;0<=c;c--){var h=c+4;var k=0<c%3;var l=[];var m=b[c];var q=a[c];for(d=q.length;d--;){var p=q[d];if(e=p.entries)for(f=e.length;f--;){var r=e[f].nd(c);if(k?r>m:r<m)m=r}for(f=4;f--;)(e=p[f])&&(k?e[h]>m:e[h]<m)&&l.push(e)}g+=l.length;b[c]=m;a[c]=l}g&&(b=ig(a,b));return b}function jg(a,b,c){var d,e;if(a.o&&(d=a.b))for(e=3;0<=e;e--){var f=b.nd(e);if(e%3?f>=d[e]:f<=d[e])if(c)d[e]=f;else{a.b=null;break}}}
gg.prototype.remove=function(a){var b,c,d,e=!1;a&&(b=a.node)&&b.b===this&&(c=b.entries)&&0<=(d=c.indexOf(a))&&(c.splice(d,1),this.m(b),jg(this,a,!1),e=!0);return e};gg.prototype.flush=function(){var a=new kg(null,NaN,this.f-this.j,this.g-this.i,this.f+this.j,this.g+this.i);a.b=this;this.head=this.a=a;this.b=null};function lg(a,b){var c=a.head,d;if(b){var e=b;if(e!==c)for(c=e;e=e.parent;)if(e.entries||1<e.a)c=e}else for(;!c.entries&&2>(d=c.a);)if(d)c=e;else break;a.head=c}
gg.prototype.eb=function(a,b,c,d,e,f){var g=[],h=this.head,k=this.a;a<=h[5]&&b<=h[6]&&(e?c>=h[7]:c>h[7])&&(f?d>=h[4]:d>h[4])&&mg(this,h,g,a,b,c,d,f||d>=k[6],e||c>=k[5]);return g};
function mg(a,b,c,d,e,f,g,h,k){var l=b.entries,m=b[7],q=b[4],p=b[5],r=b[6],v=b[8],w=b[9],z;if(l){var I=l.length;if(e>q||d>m||g<r||f<p)for(;I--;){m=l[I];q=m.nd(3);p=m.nd(0);r=m.nd(1);var G=m.nd(2);G>=e&&r>=d&&(p<g||h&&p==g)&&(q<f||k&&q==f)&&c.push(m)}else for(;I--;)c.push(l[I])}if(f>v||k&&f==v)e<w&&(z=b[1])&&mg(a,z,c,d,e,f,g,h,k),(g>w||h&&g==w)&&(z=b[3])&&mg(a,z,c,d,e,f,g,h,k);d<v&&(e<w&&(z=b[0])&&mg(a,z,c,d,e,f,g,h,k),(g>w||h&&g==w)&&(z=b[2])&&mg(a,z,c,d,e,f,g,h,k))}gg.prototype.Rc=ba(1);var ng=0;
function kg(a,b,c,d,e,f){this.c=b;a&&(this.parent=a,this.b=a.b,b&1?(c=a[8],e=a[5]):(c=a[7],e=a[8]),b&2?(d=a[9],f=a[6]):(d=a[4],f=a[9]));this[7]=c;this[5]=e;this[8]=(c+e)/2;this[4]=d;this[6]=f;this[9]=(d+f)/2}kg.prototype.a=0;function og(a,b){return a[b]||(++a.a,a[b]=new kg(a,b))}kg.prototype.removeChild=function(a){var b=a.c;this[b]===a&&(delete this[b],delete a.parent,--this.a)};kg.prototype.Rc=ba(0);function pg(a,b){(a.entries||(a.entries=[])).push(b);b.node=a}
function qg(a,b,c,d,e){var f=a[5],g=a[6];return a[7]<=b&&a[4]<=c&&(f>d||f===d&&f===a.b.a[5])&&(g>e||g===e&&g===a.b.a[6])};function rg(a,b,c,d,e,f){rg.l.constructor.apply(this,arguments)}u(rg,gg);rg.prototype.m=function(a){for(var b,c,d=this.head;a;){if(!(b=a.entries)||!b.length)if(b&&delete a.entries,!a.a&&(c=a.parent)){c.removeChild(a);d===a&&(d=c);a=c;continue}a=y}this.head!==d&&(this.head=d,lg(this))};function sg(a,b,c,d,e){if(qg(a.a,b,c,d,e))return tg(a,a.a,b,c,d,e,a.c);throw Error("Coordinates out of bounds");}rg.prototype.Dc=function(a,b){return sg(this,a,b,a,b)};
function tg(a,b,c,d,e,f,g){var h=b[8],k=b[9],l,m;g&&(e<h||(l=c>=h))&&(f<k||(m=d>=k))?c=tg(a,og(b,l|m<<1),c,d,e,f,g-1):(pg(b,c=new ug(c,d,e,f)),jg(a,c,!0),lg(a,b));return c}function ug(a,b,c,d){this.id=ng++;this[0]=b;this[1]=c;this[2]=d;this[3]=a}ug.prototype.nd=function(a){return this[a]};function vg(a){this.f=new rg(+a||10,180,90,0,0,!0);this.c=[];this.g=!1;this.a=this.b=this.N=null}t("H.geo.QuadTree",vg);n=vg.prototype;n.Lh=0;n.Yc=function(){return this.Lh};n.Hb=function(){return this.g};
n.G=function(){var a,b;if(!this.N){var c=[];!this.b&&(a=hg(this.f))&&(this.b=new J(-a[0],a[3],-a[2],a[1]));(b=this.b)&&c.push(b);var d,e,f;if(!this.a&&(f=(e=this.c).length)){a=90;var g=360;var h=-90;for(d=0;f--;){var k=e[f];a=ud(a,k[0]);g=ud(g,k[3]);h=vd(h,k[2]);d=vd(d,k[1])}this.a=new J(-a,g,-h,d-360)}(b=this.a)&&c.push(b);if(b=c[0])c[1]&&(b=b.nc(c[1],!0)),this.N=b}return this.N};
function wg(a,b,c,d,e,f){f?(f=new ug(e,-b,c+360,-d),a.c.push(f),a.g=!0,a.a&&a.a.Fc(b,c,d,e,!0,a.a)):(f=sg(a.f,c,-b,e,-d),a.b&&a.b.Fc(b,c,d,e,!0,a.b));++a.Lh;a.N=null;return f}n.Dc=function(a){var b=a.lng;a=a.lat;return wg(this,a,b,a,b,!1)};n.Sj=function(a){var b=a.Tb(),c=a.Qb();return(a=a.Hb())?wg(this,b.lat,c.lng,c.lat,b.lng,a):wg(this,b.lat,b.lng,c.lat,c.lng,a)};vg.prototype.insertBoundingBox=vg.prototype.Sj;
vg.prototype.remove=function(a){var b;if(a.node){var c=this.f.remove(a);this.b=null}else if(a=(b=this.c).indexOf(a),c=0<=a)b.splice(a,1),this.g=0<b.length,this.a=null;c&&(--this.Lh,this.N=null);return c};vg.prototype.remove=vg.prototype.remove;function xg(a,b,c,d,e,f,g){a=a.c;var h=a.length,k=[],l;if(h){var m=c+360;for(l=e+360;h--;){var q=a[h];yg(q,b,c,d,e,f,g)?k.push(q):yg(q,b,m,d,l,f,g)&&k.push(q)}}return k}
function yg(a,b,c,d,e,f,g){var h=a[3],k=a[0],l=a[1];a=a[2];return(f?k<=d:k<d)&&(g?h<=e:h<e)&&a>=b&&l>=c}function zg(a,b){var c,d,e;if(c=b.length){var f=a.length;for(d={};f--;)d[a[f].id]=1;for(;c--;)(e=b[c]).id in d||a.push(e)}}vg.prototype.Uf=function(a,b,c){var d=this.f,e=a.Tb(),f=a.Qb(),g=-e.lat;e=e.lng;var h=-f.lat;f=f.lng;!b&&g===h||!c&&e===f?a=[]:a.Hb()?(a=d.eb(-180,g,f,h,c,b),zg(a,d.eb(e,g,180,h,!1,b)),zg(a,xg(this,g,f,h,e+360,b,c))):(a=d.eb(e,g,f,h,c,b),zg(a,xg(this,g,e,h,f,b,c)));return a};
vg.prototype.intersectBoundingBox=vg.prototype.Uf;function Ag(a){return x.H.gl.flexpolyline.encode(a)}t("H.util.flexiblePolyline.encode",Ag);function Bg(a){return x.H.gl.flexpolyline.decode(a)}t("H.util.flexiblePolyline.decode",Bg);function K(a){K.l.constructor.call(this);a&&Cg(a,K,0);this.W=a||[];this.a=Dg(this,0,this.W.length)}u(K,Vf);t("H.geo.LineString",K);function Dg(a,b,c){a=a.W;var d=0;b=vd(b,0);c=ud(c,a.length);c-=2;for(b+=1;b<c;)d+=Uf(a[b],a[b+=3]);return d}K.prototype.mi=function(a,b,c){Eg(this,a,b,c,this.mi)};K.prototype.pushLatLngAlt=K.prototype.mi;function Eg(a,b,c,d,e){var f=a.W.length;b=Rf(b,e);c=Sf(c,e);a.W.push(Rf(b,e),Sf(c,e),d===B?0:Tf(d,e));f&&(a.a+=Uf(a.W[f-2],c));delete a.N;delete a.b}
K.prototype.mf=function(a,b,c){c&&Cg(c,this.mf,2);void 0===b&&(b=this.W.length);b&&(this.a-=Dg(this,a-3,a+b+3));var d=c?this.W.splice.apply(this.W,[a,b].concat(c)):this.W.splice(a,b);c&&(this.a+=Dg(this,a-3,a+c.length+3));b&&!c&&(this.a+=Dg(this,a-3,a-3));delete this.N;delete this.b;return d};K.prototype.spliceLatLngAlts=K.prototype.mf;K.prototype.Tj=function(a,b,c,d){this.mf(a,0,[b,c,d])};K.prototype.insertLatLngAlt=K.prototype.Tj;K.prototype.Ek=function(a){this.mf(a,3)};
K.prototype.removeLatLngAlt=K.prototype.Ek;K.prototype.ud=function(a){Eg(this,a.lat,a.lng,a.alt,this.ud)};K.prototype.pushPoint=K.prototype.ud;K.prototype.Dc=function(a,b){this.Tj(3*a,b.lat,b.lng,b.alt)};K.prototype.insertPoint=K.prototype.Dc;K.prototype.Ze=function(a){this.Ek(3*a)};K.prototype.removePoint=K.prototype.Ze;K.prototype.ve=function(a,b){var c=this.W,d=3*a;a=c[d];var e=c[d+1];c=c[d+2];b&&(b.lat=a,b.lng=e,b.alt=c);return b||new Wf(a,e,c)};K.prototype.extractPoint=K.prototype.ve;
K.prototype.Nl=function(a,b,c){var d=this.W;b=b||0;c=Ye(c,d.length/3);for(var e=3*b;b<c;)a(d[e++],d[e++],d[e++],b++)};K.prototype.eachLatLngAlt=K.prototype.Nl;K.isDBC=Uf;K.prototype.ih=function(a){var b=this.a;a&&(a=this.W,b+=Uf(a[a.length-2],a[1]));return b};K.prototype.getDBCs=K.prototype.ih;K.prototype.He=function(){return this.W.length/3};K.prototype.getPointCount=K.prototype.He;K.prototype.xm=function(){return this.W};K.prototype.getLatLngAltArray=K.prototype.xm;K.prototype.N=y;
K.prototype.G=function(){var a;if(!(a=this.N)){a=this.W;var b=a.length,c=3,d,e,f=y;if(3<=b){var g=d=a[0];var h=e=a[1];for(f=new J(g,h,d,e);c<b;c+=3){g=a[c-3];h=a[c-2];d=a[c];e=a[c+1];if(h>e&&180<e-h||h<e&&-180>h-e||e<h&&180>zd(e-h)){var k=h;h=e;e=k}g<d&&(k=g,g=d,d=k);bg(f.ia,f.aa,f.ma,f.da,g,h,d,e,f)}}a=this.N=f}return a};K.prototype.getBoundingBox=K.prototype.G;K.prototype.hn=function(){return this.N!==y};K.prototype.hasBoundingBox=K.prototype.hn;
function Cg(a,b,c){for(var d=a.length,e=!(d%3),f;e&&d;)e=!(E(a[--d]=Tf((f=a[d])===B?0:f))||E(a[--d]=Sf(a[d]))||E(a[--d]=Rf(a[d])));if(!e&&b)throw new D(b,c,a);}function Fg(a){var b=new K,c=0,d=a.length;if(d%2)throw new D(Fg,0,a);for(;c<d;)Eg(b,a[c++],a[c++],0,Fg);return b}K.fromLatLngArray=Fg;K.prototype.na=function(a){var b=this===a,c;if(!b&&(b=C(a,K))){var d=this.W;a=a.W;for(b=(c=d.length)===a.length;b&&c--;)b=d[c]==a[c]}return b};K.prototype.equals=K.prototype.na;
function Gg(a,b){return a.a-b.a}
function Hg(a,b){var c=a.W,d=-2,e=[],f;var g=a.b;if(!g){g=a.b=new vg;var h=0;var k=a.W;var l=k.length;for(f=0;f<l;f+=3){var m=k[f];var q=k[f+1];if(f){if(r<q){var p=r;var r=q}else p=q;if(w<m)var v=m;else{v=w;var w=m}p=wg(g,v,p,w,r,180<r-p);p.a=h++}w=m;r=q}}g=g.Uf(b).sort(Gg);k=g.length;for(b=0;b<k;b++){h=g[b];h=h.a;l=3*h;if(h>d+1){var z=[c[l],c[l+1]];e.push(z)}d=h;z.push(c[l+3],c[l+4])}if(a.a){c=[];d=e.length;for(b=0;b<d;b++)if(z=e[b],g=z.length){k=[];for(a=0;a<g;a+=2)h=z[a],l=z[a+1],k.push(h,l),f=
z[a-1],a&&Uf(l,f)&&(c.push(k),k=[],f+=0>f?360:-360,k.push(z[a-2],f,h,l));c.push(k)}e=c}return e}n=K.prototype;n.qb="LineString";n.Qc=function(a,b){var c=this.W,d=c.length,e;if(d){a.push("(");for(e=0;e<d;e+=3)e&&a.push(","),a.push(c[e+1]," ",c[e]);b&&(c[0]!==c[d-3]||c[1]!==c[d-2])&&a.push(",",c[1]," ",c[0]);a.push(")")}else a.push("EMPTY");return a};n.Ob="LineString";n.ed=function(){var a=[],b=this.W,c=b.length,d;for(d=0;d<c;d+=3)a.push([b[d+1],b[d],b[d+2]]);return a};
n.wc=function(){var a=this.W,b;if(this.G().Hb()){a=a.slice();var c=1;for(b=a.length;c<b;c+=3)0>a[c]&&(a[c]+=360)}return a};n.ro=function(a){a=void 0===a?5:a;for(var b=this.W,c=b.length,d=[],e=0;e<c;e+=3)d.push([b[e],b[e+1],b[e+2]]);return Ag({polyline:d,precision:a,thirdDim:2,thirdDimPrecision:a})};K.prototype.toFlexiblePolyline=K.prototype.ro;
function Ig(a){var b=Bg(a);a=b.polyline;var c=b.thirdDim;b=2===c;c=0===c;if(!a)throw new D(Ig,0,"data");if(b||c){c=a.length;var d=Array(3*c);for(var e=0,f=0;e<c;e++)d[f++]=a[e][0],d[f++]=a[e][1],d[f++]=b?a[e][2]:0}if(!d)throw new D(Ig,0,"only ALTITUDE and ABSENT dimension types are supported");return new K(d)}K.fromFlexiblePolyline=Ig;function Jg(a){Jg.l.constructor.call(this);void 0!==a&&(this.data=a)}u(Jg,F);t("H.map.Feature",Jg);Jg.prototype.getData=function(){return this.data};Jg.prototype.getData=Jg.prototype.getData;Jg.prototype.u=function(){Jg.l.u.call(this);delete this.data};function Kg(){}t("H.map.provider.Invalidations",Kg);Kg.MARK_INITIAL=Td;Kg.prototype.update=function(a,b){b!==Lg.NONE&&(this.a=a,b&Lg.SPATIAL&&(this.f=a),b&Lg.VISUAL&&(this.g=a),b&Lg.ADD&&(this.b=a),b&Lg.REMOVE&&(this.c=a),b&Lg.Z_ORDER&&(this.i=a),b&Lg.VOLATILITY&&(this.j=a))};Kg.prototype.update=Kg.prototype.update;Kg.prototype.Dm=function(){return this.a};Kg.prototype.getMark=Kg.prototype.Dm;Kg.prototype.a=Td;Kg.prototype.mn=function(a){return this.a>a};Kg.prototype.isAny=Kg.prototype.mn;
Kg.prototype.g=Td;Kg.prototype.Zd=function(a){return this.g>a};Kg.prototype.isVisual=Kg.prototype.Zd;Kg.prototype.f=Td;Kg.prototype.Eh=function(a){return this.f>a};Kg.prototype.isSpatial=Kg.prototype.Eh;Kg.prototype.b=Td;Kg.prototype.Uj=function(a){return this.b>a};Kg.prototype.isAdd=Kg.prototype.Uj;Kg.prototype.c=Td;Kg.prototype.Wf=function(a){return this.c>a};Kg.prototype.isRemove=Kg.prototype.Wf;Kg.prototype.i=Td;Kg.prototype.Fh=function(a){return this.i>a};Kg.prototype.isZOrder=Kg.prototype.Fh;
Kg.prototype.j=Td;Kg.prototype.qn=function(a){return this.j>a};Kg.prototype.isVolatility=Kg.prototype.qn;var Lg={NONE:0,VISUAL:1,SPATIAL:2,ADD:4,REMOVE:8,Z_ORDER:16,VOLATILITY:32};Kg.Flag=Lg;function Mg(a,b,c){Mg.l.constructor.call(this,a);this.oldValue=c;this.newValue=b}u(Mg,qd);t("H.util.ChangeEvent",Mg);function L(a){tc(this,L);L.l.constructor.call(this,a?a.data:B);this.L=Ng.next();if(a){var b="min";Bc(a[b])&&(this.s=a[b]);b="max";Bc(a[b])&&(this.v=a[b]);b="visibility";b in a&&(this.c=!!a[b]);b="volatility";b in a&&(this.I=!!a[b]);b="zIndex";b in a&&(this.o=+a[b]||0);b="provider";b in a&&!C(a[b],M)&&(this.a=a[b],this.va(Lg.ADD))}}u(L,Jg);t("H.map.Object",L);var Ng=new $e(1),Og={ANY:31,OVERLAY:1,SPATIAL:2,MARKER:4,DOM_MARKER:8,GROUP:16};L.Type=Og;L.prototype.hb=function(){return this.L};
L.prototype.getId=L.prototype.hb;L.prototype.Di=function(a){if(!Bc(a)&&!yc(a))throw new D(this.Di,0,"id must be a number or a string");this.m=a;return this};L.prototype.setRemoteId=L.prototype.Di;L.prototype.Sm=function(){return this.m};L.prototype.getRemoteId=L.prototype.Sm;L.prototype.s=-1/0;L.prototype.v=1/0;L.prototype.Em=function(){return this.v};L.prototype.getMax=L.prototype.Em;L.prototype.Gm=function(){return this.s};L.prototype.getMin=L.prototype.Gm;L.prototype.c=!0;
L.prototype.yb=function(a){var b=this.c;(a=!!a)^b&&(this.c=a,this.invalidate(Lg.VISUAL));return this};L.prototype.setVisibility=L.prototype.yb;L.prototype.Bc=function(a){for(var b=this,c;(c=b.c)&&a&&(b=b.Za););return c};L.prototype.getVisibility=L.prototype.Bc;L.prototype.I=!1;L.prototype.Rf=function(a){for(var b=this,c;!(c=b.I)&&a&&(b=b.Za););return c};L.prototype.getVolatility=L.prototype.Rf;L.prototype.Zk=function(a){var b=this.I;b^a&&(this.I=!b,this.invalidate(Lg.VOLATILITY));return this};
L.prototype.setVolatility=L.prototype.Zk;L.prototype.o=B;L.prototype.Kj=function(){return this.o};L.prototype.getZIndex=L.prototype.Kj;L.prototype.jf=function(a){a!==this.o&&(this.bf(),this.o=a,this.invalidate(Lg.Z_ORDER));return this};L.prototype.setZIndex=L.prototype.jf;L.prototype.F=B;function Pg(a){var b=a.F,c,d;if(!b){var e=(c=a.o)!==B;(b=a.Za)?(b=Pg(b).slice(),b[0]|=e):b=[e|0];b.push(c||0,0>(d=a.Hi)?a.L:d);a.F=b}return b}L.prototype.bf=function(){this.F=B};
function Qg(a,b,c){var d,e;if(!c||a[0]|b[0]){var f=a.length;var g=b.length;var h=ud(f,g);var k=1;for(e=1+c;k<h;k+=e)if(d=a[k]-b[k])return d}return c?0:f-g}function Rg(a,b){return a.jj(b)}L.compareZOrder=Rg;L.prototype.jj=function(a){return this.yg-a.yg||Qg(Pg(this),Pg(a),!1)};L.prototype.compareZOrder=L.prototype.jj;n=L.prototype;n.previousSibling=y;n.nextSibling=y;n.Hi=-1;n.Za=y;n.Im=function(){return this.Za};L.prototype.getParentGroup=L.prototype.Im;
L.prototype.kc=function(){for(var a=this,b;b=a.Za;)a=b;return a};L.prototype.getRootGroup=L.prototype.kc;L.prototype.contains=function(a){return this===a};L.prototype.contains=L.prototype.contains;L.prototype.ha=function(a){if(this.Za)throw new Xc(this.ha,"Not allowed for a child of a group");L.l.ha.call(this,a)};L.prototype.setParentEventTarget=L.prototype.ha;L.prototype.a=y;L.prototype.pa=function(){return this.a};L.prototype.getProvider=L.prototype.pa;
L.prototype.ge=function(a,b){var c=this.a,d;if(d=c!==a){if(b&&(c&&!C(c,M)||a&&!C(a,M)))throw new Xc(b,"Only LocalObjectProvider allows an object transfers");b=this.type!==Og.GROUP;c&&(this.invalidate(Lg.REMOVE),b&&c.Ka(this));if(this.a=a)b&&a.ca(this),this.ka=y,this.invalidate(Lg.ADD)}return d};L.prototype.Sb=function(){return this.ka||(this.ka=new Kg)};L.prototype.getInvalidations=L.prototype.Sb;L.prototype.va=function(a){var b=this.pa(),c;(c=!!b)&&b.invalidateObject(this,a);return c};
L.prototype.invalidate=L.prototype.va;L.prototype.u=function(){this.Za&&this.Za.Ka(this);L.l.u.call(this)};L.prototype.setData=function(a){this.data=a;return this};L.prototype.setData=L.prototype.setData;L.prototype.Pc=function(a){if(a&&!Ba(a))throw new D(L.prototype.Pc,0,"opt_callback must be a function");a={type:"Feature",properties:Sg(this,a?a(this.data):this.data,!!a),geometry:this.$().Pc()};this.m&&(a.id=this.m);return a};L.prototype.toGeoJSON=L.prototype.Pc;
function Sg(a,b,c){if(null===b||b===B)return null;if(0<=Object.keys(b).length&&"[object Object]"!==Object.prototype.toString.call(b))throw Error(Tg(a,c));try{return JSON.stringify(b),b}catch(d){throw Error(Tg(a,c));}}function Tg(a,b){return"Object Remote-Id: "+a.m+" - "+(b?"The value returned by the callback is not a valid JSON object and cannot be set as Feature properties.":"The given object data is not a valid JSON object and cannot be set as Feature properties.")}
L.prototype.V=function(){return{id:this.L,properties:{min:this.s,max:this.v,zIdx:this.o,sIdx:this.Hi,parent:this.Za?this.Za.hb():0,visible:this.Bc(),"volatile":this.Rf()},type:"Feature"}};L.prototype.forWorkerMessage=L.prototype.V;function Ug(a){var b;if(a){var c=Vg;for(b=C(a,Ug);c--;){var d=Wg[c];if(a.hasOwnProperty(d)){var e=a[d];if(b)this[d]=e;else{if((e=Xg[c](e))===Yg)throw new D(Ug,0,d+": "+a[d]);e!==this[d]&&e!==B&&(this[d]=e)}}}c=b?a.Le:this.lineWidth&&We(this.strokeColor);c||(this.Le=c);c=b?a.Ub:We(this.fillColor);c||(this.Ub=c);c=b?a.Ke:"none"!==this.strokeColor&&this.lineWidth;c||(this.Ke=c)}nc(this)}t("H.map.SpatialStyle",Ug);Ug.prototype.Ub=!0;Ug.prototype.Le=!0;Ug.prototype.Ke=!0;var Wg=[];
Ug.prototype[Wg[0]="strokeColor"]="rgba(0,85,170,.6)";Ug.prototype[Wg[1]="fillColor"]="rgba(0,85,170,.4)";Ug.prototype[Wg[2]="lineWidth"]=2;Ug.prototype[Wg[3]="lineCap"]="round";Ug.prototype[Wg[4]="lineJoin"]="miter";Ug.prototype[Wg[5]="miterLimit"]=1;Ug.prototype[Wg[6]="lineDash"]=ef;Ug.prototype[Wg[7]="lineDashOffset"]=0;Ug.prototype[Wg[8]="lineHeadCap"]=B;Ug.prototype[Wg[9]="lineTailCap"]=B;var Vg=Wg.length;
Ug.prototype.na=function(a){var b=this===a;if(!b&&a){for(b=0;b<Vg;b++){var c=Wg[b];if(this[c]!==a[c])break}b=b===Vg}return b};Ug.prototype.equals=Ug.prototype.na;Ug.prototype.Bj=function(a){if(a){var b={};Va(b,this,a)}else b=this;return new Ug(b)};Ug.prototype.getCopy=Ug.prototype.Bj;
var Yg=nc({}),Xg=[function(a){return a?mc(a):Yg},function(a){return a?mc(a):Yg},function(a){return 0<=a&&100>=a?+a:Yg},function(a){a=mc(a);return"butt"===a||"square"===a||"round"===a||"arrow-head"===a||"arrow-tail"===a?a:Yg},function(a){return"round"===a||"bevel"===a||"miter"===a?a:Yg},function(a){return 0<a&&100>=a?+a:Yg},function(a){return a&&a.every&&a.every(Cc)?a:Yg},function(a){return E(+a)?Yg:+a},function(a){return sc(a)?Xg[3](a):B},function(a){return sc(a)?Xg[3](a):B}];Ug.MAX_LINE_WIDTH=100;
var Zg=new Ug;Ug.DEFAULT_STYLE=Zg;var $g="fillColor strokeColor lineWidth lineCap lineJoin miterLimit lineDashOffset lineDash lineTailCap lineHeadCap".split(" ");Ug.prototype.V=function(){for(var a={},b=$g.length,c;b--;)c=$g[b],a[c]=this[c];return a};Ug.prototype.forWorkerMessage=Ug.prototype.V;function ah(a){var b;if(a){var c=C(a,ah);for(b in a)if(b in this){var d=a[b];d!==this[b]&&("fillColor"===b||0<(d=+d))&&(this[b]=d)}a=c?a.Ub:!!(We(this.fillColor)&&this.width&&this.width);a||(this.Ub=a)}nc(this)}t("H.map.ArrowStyle",ah);ah.prototype.Ub=!0;ah.prototype.fillColor="rgba(255,255,255,.75)";ah.prototype.width=1.2;ah.prototype.length=1.6;ah.prototype.frequency=5;ah.prototype.Aj=function(){return new ah(this)};
ah.prototype.na=function(a){var b=this===a;!b&&a&&(b=a.width===this.width&&a.fillColor===this.fillColor&&a.length===this.length&&a.frequency===this.frequency);return b};ah.prototype.equals=ah.prototype.na;function bh(a,b){var c;bh.l.constructor.call(this,b);b&&this.dd(b.style);a&&(this.i=!0);b&&(c=b.arrows)&&this.Ok(c)}u(bh,L);t("H.map.Spatial",bh);bh.prototype.type=Og.SPATIAL;bh.prototype.yg=0;bh.prototype.style=Zg;bh.prototype.ya=function(){return this.style};bh.prototype.getStyle=bh.prototype.ya;bh.prototype.dd=function(a){var b=!0;a?this.style=C(a,Ug)?a:new Ug(a):this.style?delete this.style:b=!1;b&&this.invalidate(Lg.VISUAL);return this};bh.prototype.setStyle=bh.prototype.dd;
bh.prototype.Wl=function(){return this.g};bh.prototype.getArrows=bh.prototype.Wl;bh.prototype.Ok=function(a){var b=this.g,c=!1;!a&&b?(delete this.g,c=!0):!a||b&&b.na(a)||(this.g=new ah(a),c=!0);c&&"none"!==this.style.strokeColor&&this.va(1);return this};bh.prototype.setArrows=bh.prototype.Ok;function ch(a,b){var c=!1,d=!1,e;if(b.length){for(c=0;c<b.length;c++)if(b[c]!==dh){d=!0;break}b=a.style;c=d?b.Le||b.Ub&&a.i||(e=a.g||!1)&&b.Ke&&e.Ub:b.Ub}return c&&a.Bc(!0)}bh.prototype.i=!1;bh.prototype.on=function(){return this.i};
bh.prototype.isClosed=bh.prototype.on;bh.prototype.getGeometriesForTile=bh.prototype.Pd;bh.prototype.nh=function(){return y};bh.prototype.getLabels=bh.prototype.nh;function eh(a,b){eh.l.constructor.call(this,a,b)}u(eh,bh);t("H.map.GeoShape",eh);eh.prototype.getBoundingBox=eh.prototype.G;function fh(a,b,c,d){var e=[],f=b.length,g;for(g=0;g<f;g++){var h=b[g];h.length&&e.push(gh(a,h,c,d))}return e}function gh(a,b,c,d){var e,f=[],g=b.length,h=0;a.U=0;for(e=e||0;h<g;)f.push(hh(a,b[h++],b[h++],e,d));c&&f.push(hh(a,b[0],b[1],e,d));return f}function hh(a,b,c,d,e){var f=a.U;f&&180<zd(f-c)&&(c+=0>f?-360:360);a.U=c;return e.Gh(b,c+d)}
function ih(a,b,c){for(var d=b,e,f=a.length+b,g,h;d--;){b=a[d];g=b.length;for(e=Array(g);g--;)h=b[g],e[g]=new H(h.x+c,h.y);a[--f]=e}}var jh=new K([0,0,0,0,0,0,0,0,0]);function kh(a){tc(this,kh);kh.l.constructor.call(this);this.oa=lh(this,a,this.constructor,0)}u(kh,Vf);t("H.geo.MultiGeometry",kh);kh.prototype.splice=function(a,b,c){a=[a];b!==B&&a.push(b);c&&(b=lh(this,c,this.splice,2),a=a.concat(b));this.N=y;return this.oa.splice.apply(this.oa,a)};kh.prototype.splice=kh.prototype.splice;kh.prototype.pc=function(a){var b=this.oa.length;if(!(0<=a&&a<b))throw new ie(this.pc,a,[0,b-1]);this.N=y;return this.oa.splice(a,1)[0]};kh.prototype.removeAt=kh.prototype.pc;
kh.prototype.remove=function(a){a=this.oa.indexOf(a);if(0<=a){var b=this.oa.splice(a,1)[0];this.N=y}return b||y};kh.prototype.remove=kh.prototype.remove;kh.prototype.qm=function(){return this.oa};kh.prototype.getGeometries=kh.prototype.qm;kh.prototype.push=function(a){var b=lh(this,[a],this.push,0)[0];this.N&&(this.N=this.N.nc(a.G()));this.oa.push(b)};kh.prototype.push=kh.prototype.push;
kh.prototype.G=function(){var a;if(!(a=this.N)){a=y;var b,c;if(this.oa.length)for(a=this.oa[0].G(),c=1;c<this.oa.length;c++)if(b=this.oa[c].G())a=a?a.nc(b):b}return this.N=a};kh.prototype.getBoundingBox=kh.prototype.G;kh.prototype.N=y;function lh(a,b,c,d){var e,f=[];if(!xc(b))throw new D(c,d);for(e=0;e<b.length;e++)if(a.a(b[e]))f.push(a.b(b[e]));else throw new D(c,d);return f}kh.prototype.b=function(a){return a};
kh.prototype.na=function(a){var b=this===a,c;if(!b&&(b=C(a,this.constructor))){var d=this.oa;a=a.oa;for(b=(c=d.length)===a.length;b&&c--;)b=d[c].na(a[c])}return b};kh.prototype.equals=kh.prototype.na;n=kh.prototype;n.Qc=function(a){var b=this.oa,c=b.length,d,e,f=!1;if(c){a.push("(");for(d=0;d<c;d++)(e=0<d&&f)&&a.push(","),b[d].Qc(a),"EMPTY"===a[a.length-1]?a.splice(-1-e,1+e):f=!0;f?a.push(")"):a.splice(-1,1,"EMPTY")}else a.push("EMPTY");return a};
n.toString=function(){return this.Qc([this.qb.toUpperCase()," "]).join("")};n.wc=function(){for(var a=[],b=this.oa,c=b.length;c--;)a[c]=b[c].wc();return a};n.V=function(){var a=kh.l.V.call(this);a.type=this.qb;return a};n.ed=function(){for(var a=[],b=this.oa,c=b.length;c--;)a[c]=b[c].ed();return a};function mh(a){mh.l.constructor.call(this,a)}u(mh,kh);t("H.geo.MultiLineString",mh);mh.prototype.a=function(a){return C(a,K)};mh.prototype.qb="Multi"+K.prototype.qb;mh.prototype.Ob="Multi"+K.prototype.Ob;function nh(a,b){nh.l.constructor.call(this,!1,b);this.ba(a)}u(nh,eh);t("H.map.Polyline",nh);nh.prototype.G=function(){return this.gb.G()};nh.prototype.getBoundingBox=nh.prototype.G;nh.prototype.gb=y;nh.prototype.ba=function(a){var b=this.ba,c,d;if(C(a,mh)){var e=a.oa;if(c=e.length)for(d=0;d<c;d++)oh(e[d],b);else throw new D(b,0);}else oh(a,b);this.pd=!!e;this.gb=a;this.va(Lg.SPATIAL);return this};nh.prototype.setGeometry=nh.prototype.ba;nh.prototype.$=function(){return this.gb};
nh.prototype.getGeometry=nh.prototype.$;nh.prototype.clip=function(a){var b=this.gb;return Hg(this.pd?b.oa[0]:b,a)};nh.prototype.clip=nh.prototype.clip;nh.prototype.Pd=function(a){var b=this.gb;var c,d=[];if(this.pd)for(b=b.oa,c=b.length;c--;)ph(this,b[c],a,d);else ph(this,b,a,d);return d.length?d:B};nh.prototype.getGeometriesForTile=nh.prototype.Pd;function oh(a,b){if(!C(a,K)||2>a.He())throw new D(b,0);}
function ph(a,b,c,d){var e=Hg(b,c.Lf());if(e.length&&(b=c.Nf(),a=fh(a,e,!1,b),e=a.length)){var f=c.Je();b=b.w;c.x||ih(a,e,-b);c.x===(1<<c.z)-1&&ih(a,e,b);c=qh(a,f.left,f.top,f.right,f.bottom,!1);c.length&&d.push(new rh(c))}}nh.prototype.V=function(){var a=nh.l.V.call(this),b=a.properties;a.geometry=this.$().V();b.style=this.ya().V();b.height=0;return a};nh.prototype.forWorkerMessage=nh.prototype.V;function qh(a,b,c,d,e,f){var g,h,k=a.length,l,m;if(k)for(g=[];k--;){var q=a[k];var p=q.length;var r=0;for(l=1;l<p;l++)if(m=sh(q[l-1],q[l],c,b,d,e)){var v=m[0];var w=m[1];r&&r.na(v)?h.push(w):g.push(h=m);r=w;f&&(l=p,k=0)}}else g=a;return g}t("H.math.clipping.clipStrips",qh);
function sh(a,b,c,d,e,f){var g=a.x;a=-a.y;var h=b.x;b=-b.y;c=-c;f=-f;if(g>h){if(h>e||g<d)return;var k=g;var l=a;g=h;a=b;h=k;b=l;k=1}else if(g>e||h<d)return;if(a>b){if(b>c||a<f)return;var m=1;a=-a;b=-b;l=f;f=-c;c=-l}else if(a>c||b<f)return;if(g<d){if((a+=(d-g)*(b-a)/(h-g))>c)return;g=d}if(a<f){if((g+=(f-a)*(h-g)/(b-a))>e)return;a=f}h>e&&(b=a+(e-g)*(b-a)/(h-g),h=e);b>c&&(h=g+(c-a)*(h-g)/(b-a),b=c);m&&(a=-a,b=-b);return k?[new H(h,-b),new H(g,-a)]:[new H(g,-a),new H(h,-b)]}
function th(a,b,c){a=uh(a,!0);b=uh(b,!1);var d,e;var f={};var g=d=1;switch(~~(c||0)){case 1:g=d=0;break;case 2:d=0;g=1;break;case 3:d=1,g=0}c=d;var h=g;if(b&&a){b.Cf=vh(b.x,b.y,null,wh(b));a.Cf=vh(a.x,a.y,null,wh(a));for(g=b;g.next;g=g.next)if(!g.eb)for(d=a;d.next;d=d.next)if(!d.eb){var k=xh(g.next);var l=xh(d.next);if(e=yh(g,k,d,l,f)){e=f.wl;var m=f.xl;var q=f.wo;var p=f.xo;e=vh(q,p,null,null,null,null,!0,0,0,e);zh(e,g,k);k=vh(q,p,null,null,null,null,!0,0,0,m);zh(k,d,l);e.Yh=k;k.Yh=e}}f=be(b,Ah(a));
c&&(f=!f);for(g=b;g;g=g.next)g.eb&&(g.$g=f,f=!f);f=be(a,Ah(b));h&&(f=!f);for(d=a;d.next;d=d.next)d.eb&&(d.$g=f,f=!f);Bh(b);for(Bh(a);(a=Ch(b))!=b;){for(c=null;!a.wg;a=a.Yh){for(f=a.$g;;){c=vh(a.x,a.y,c);c.artificial=a.eb||a.nn;a.wg=1;a=f?a.next:a.Wb;if(!a)break;if(a.eb){a.wg=1;break}}if(!a)break}c.Zh=r;var r=c}return r}}t("H.math.clipping.clipPolygon",th);
function vh(a,b,c,d,e,f,g,h,k,l){a={x:a,y:b,next:c||null,Wb:d||null,Zh:e||null,Yh:f||null,eb:!!g,$g:h||0,wg:k||0,alpha:l||0};d&&(a.Wb.next=a);c&&(a.next.Wb=a);return a}function xh(a){for(;a&&a.eb;)a=a.next;return a}function wh(a){if(a)for(;a.next;)a=a.next;return a}function Ch(a){var b=a;if(b){do b=b.next;while(b!=a&&(!b.eb||b.eb&&b.wg))}return b}function Bh(a){var b=wh(a);b.Wb.next=a;a.Wb=b.Wb}
function yh(a,b,c,d,e,f){var g,h=b.x-a.x,k=b.y-a.y;var l=d.x-c.x;var m=d.y-c.y;var q=h*m-k*l;if(!q)return 0;l=((c.x-a.x)*m-(c.y-a.y)*l)/q;q=(k*(c.x-a.x)-h*(c.y-a.y))/q;if(0>l||1<l||0>q||1<q)return 0;0===l?g=a:1===l?g=b:0===q?g=c:1===q&&(g=d);if(g&&!f)return g.x+=2.480549651603763E-5,g.y+=7.321997314118067E-5,g.Cf&&(g.Cf.x=g.x,g.Cf.y=g.y),yh(a,b,c,d,e);e.wo=a.x+l*h;e.xo=a.y+l*k;e.wl=l;e.xl=q;return 1}function Ah(a){for(var b=[];a;)b.push(a.x,a.y),a=a.next;return b}
function zh(a,b,c){for(b=b.next;b!==c&&b.alpha<=a.alpha;)b=b.next;a.next=b;a.Wb=b.Wb;a.next.Wb=a;a.Wb.next=a}function uh(a,b){for(var c,d=null,e=0,f=a.length;e<f;e++){c=vh(a[e].x,a[e].y,d);c.nn=b;if(c.next=d)d.Wb=c;d=c}return d};function N(a,b){var c;N.l.constructor.call(this);C(a,K,N,0);if(b!==B&&xc(b,N,1)){for(c=0;c<b.length;c++)C(b[c],K,N,1,"index "+c);this.Pa=b}else this.Pa=[];this.fb=a;this.a=[]}u(N,Vf);t("H.geo.Polygon",N);function Dh(a){var b=N,c=K,d=a.ia,e=a.aa,f=a.ma,g=a.da;e=[d,e,B,d,g,B,f,g,B,f,e,B];180<=a.Gb()&&(e.splice(9,0,f,a=a.ob().lng,B),e.splice(3,0,d,a,B));return new b(new c(e))}var Eh={NORTH:90,SOUTH:-90};N.Direction=Eh;N.prototype.sd=Eh.NORTH;
N.prototype.Vk=function(a){this.sd!==a&&(this.N=y,this.a.length=0,this.sd=a);return this};N.prototype.setPoleCovering=N.prototype.Vk;N.prototype.Nm=function(){return this.sd};N.prototype.getPoleCovering=N.prototype.Nm;N.prototype.km=function(){return this.fb};N.prototype.getExterior=N.prototype.km;N.prototype.Sk=function(a){if(!C(a,K))throw new D(this.Sk,0,a);this.fb=a;this.N=y};N.prototype.setExterior=N.prototype.Sk;N.prototype.um=function(){return this.Pa};N.prototype.getInteriors=N.prototype.um;
N.prototype.vg=function(a,b,c){var d=arguments.length,e;for(e=2;e<d;e++)C(arguments[e],K,this.vg,e);var f=this.Pa.splice.apply(this.Pa,arguments);for(e=2;e<d;e++)arguments[e]=B;this.a.splice.apply(this.a,arguments);return f};N.prototype.spliceInteriors=N.prototype.vg;N.prototype.Zn=function(a){return this.vg(a,1)[0]};N.prototype.removeInteriorAt=N.prototype.Zn;N.prototype.Yn=function(a){a=this.Pa.indexOf(a);return 0>a?B:this.vg(a,1)[0]};N.prototype.removeInterior=N.prototype.Yn;
N.prototype.Ck=function(a){if(!C(a,K))throw new D(this.Ck,0,a);this.Pa.push(a)};N.prototype.pushInterior=N.prototype.Ck;N.prototype.G=function(){var a=this.N;a||(this.N=a=Fh(this.fb,this.sd));return a};N.prototype.getBoundingBox=N.prototype.G;n=N.prototype;n.zj=function(a){var b=this.Pa.length;if(0>a||a>=b)throw new ie(this.zj,a,[0,b-1]);(b=this.a[a])||(this.a[a]=b=Fh(this.Pa[a],this.sd));return b};n.fb=y;n.Pa=[];
function Fh(a,b){var c,d,e;if(e=a.G())(c=a.ih(!0))&&(d=a.He())&&(e=e.nc(dg([a.ve(0),a.ve(d-1)],!0),!0)),360===e.Gb()&&1===c%2&&(e=e.ad(b,0));return e}n.qb="Polygon";n.Qc=function(a){var b=this.Pa,c=b.length,d;if(this.fb.He()){a.push("(");this.fb.Qc(a,!0);for(d=0;d<c;d++)b[d].He()&&(a.push(","),b[d].Qc(a,!0));a.push(")")}else a.push("EMPTY");return a};n.Ob="Polygon";
n.ed=function(){var a,b=[],c=this.Pa,d=this.fb.ed();d[0].toString()!==d[d.length-1].toString()&&d.push(d[0]);b.push(d);for(a=0;a<c.length;a++)d=c[a].ed(),d[0].toString()!==d[d.length-1].toString()&&d.push(d[0]),b.push(d);return b};n.V=function(){var a=N.l.V.call(this);this.G().Hb()&&(a.type="Multi"+a.type);return a};n.wc=function(){var a=[],b=this.Pa,c=b.length;for(a.push(this.fb.wc());c--;)a[c+1]=b[c].wc();return this.G().Hb()?[a]:a};
n.na=function(a){var b=a.Pa,c=this.Pa.length,d=b.length;a=this.fb.na(a.fb)&&c===d;for(d=0;a&&d<c;)a=a&&this.Pa[d].na(b[d]),d++;return a};function Gh(a,b,c){var d=void 0===d?!0:d;var e=a.Pa,f=Hh.bind(null,b,c);return ae(b,c,a.fb.W,0,!0,3)!==$d.NONE?d?!e.some(f):!0:!1}function Hh(a,b,c){return ae(a,b,c.W,0,!0,3)===$d.SURFACE}
function Ih(a,b){b=b.W;a=a.fb.W;var c,d,e=b.length-3,f=a.length-3,g={};for(c=0;c<e;c+=3){var h=b[c];var k=b[c+1];var l=b[c+3];var m=b[c+4];for(d=0;d<f;d+=3){var q=a[d];var p=a[d+1];var r=a[d+3];var v=a[d+4];if(yh({x:k,y:h},{x:m,y:l},{x:p,y:q},{x:v,y:r},g,!0))return!0}}return!1}
function Jh(a,b){var c=b.fb,d=b.Pa,e=d.length,f=c.W,g=f.length,h=a.fb.W,k=h.length;if(Ih(a,c))return!0;for(c=0;c<g;c+=3)if(Gh(a,f[c],f[c+1]))return!0;for(c=0;c<k;c+=3)if(Gh(b,h[c],h[c+1]))return!0;for(c=0;c<e;c++)if(Ih(a,d[c]))return!0;return!1};function Kh(a){Kh.l.constructor.call(this,a)}u(Kh,kh);t("H.geo.MultiPolygon",Kh);Kh.prototype.a=function(a){return C(a,N)};Kh.prototype.qb="Multi"+N.prototype.qb;Kh.prototype.Ob="Multi"+N.prototype.Ob;function rh(a,b,c){this.paths=this.a=a;b!==B&&(this.interiorsIndex=this.b=b);c!==B&&(this.outlinesIndex=this.c=c)}rh.prototype.interiorsIndex=rh.prototype.b=Sd;rh.prototype.outlinesIndex=rh.prototype.c=Sd;var dh=oc(new rh([])),Lh=nc([]);function Mh(a,b){var c=b&&(+b.extrusion||+b.extrude),d=b&&+b.elevation,e=0;Mh.l.constructor.call(this,!0,b);0<d&&(e+=d,this.f=d);0<c&&(e+=c,this.j=c);if(e>Nh)throw new ie(Mh,e,[0,Nh]);C(a,K)?this.ba(new N(a)):this.ba(a)}u(Mh,eh);t("H.map.Polygon",Mh);Mh.prototype.j=0;Mh.prototype.f=0;Mh.prototype.gb=y;var Nh=2047;Mh.MAX_EXTRUDE_HEIGHT=Nh;Mh.prototype.ti=function(a){var b=+a;if(b!==a)throw new D(this.ti,0,a);if(0>b||this.f+b>Nh)throw new ie(this.ti,this.f+b,[0,Nh]);this.j=b;this.va(Lg.SPATIAL)};
Mh.prototype.setExtrusion=Mh.prototype.ti;Mh.prototype.lm=function(){return this.j};Mh.prototype.getExtrusion=Mh.prototype.lm;Mh.prototype.si=function(a){var b=+a;if(b!==a)throw new D(this.si,0,a);if(0>b||this.j+b>Nh)throw new ie(this.si,this.j+b,[0,Nh]);this.f=b;this.va(Lg.SPATIAL)};Mh.prototype.setElevation=Mh.prototype.si;Mh.prototype.jm=function(){return this.f};Mh.prototype.getElevation=Mh.prototype.jm;Mh.prototype.$=function(){return this.gb};Mh.prototype.getGeometry=Mh.prototype.$;
Mh.prototype.ba=function(a){if(a===y||C(a,N))var b=!1;else C(a,Kh,this.ba,0),b=!0;this.pd=b;b=this.gb;this.gb=a;b!==y&&this.va(Lg.SPATIAL);return this};Mh.prototype.setGeometry=Mh.prototype.ba;Mh.prototype.G=function(){return this.$().G()};Mh.prototype.getBoundingBox=Mh.prototype.G;
Mh.prototype.Pd=function(a){var b,c=this.$(),d,e;if(this.pd){c=c.oa;var f=0;for(e=c.length;f<e;f++)if(d=Oh(this,c[f],a,c[f].sd))b||(b=[]),b.push(d)}else d=this.ab,d===B&&(d=this.pd?Eh.NORTH:this.$().sd),(d=Oh(this,c,a,d))&&(b=[d]);return b};Mh.prototype.getGeometriesForTile=Mh.prototype.Pd;
function Oh(a,b,c,d){var e,f,g=0,h=!0;if(e=Ph(a,b.fb,c,d,b.G())){var k=new rh(e);var l=b.Pa;if(f=l.length)for(k.b=k.a.length;g<f;g++)if(e=Ph(a,l[g],c,d,b.zj(g)))k.a=k.a.concat(e);


# In[ ]:



{
   "schemaVersion": 2,
   "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
   "config": {
      "mediaType": "application/vnd.docker.container.image.v1+json",
      "size": 33352,
      "digest": "sha256:f3600c9576fbb6a3676b76ff8c1b87811f945bc0d8f9815e6b1020790034bfe1"
   },
   "layers": [
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 26692096,
         "digest": "sha256:423ae2b273f4c17ceee9e8482fa8d071d90c7d052ae208e1fe4963fceb3d6954"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 35365,
         "digest": "sha256:de83a2304fa1f7c4a13708a0d15b9704f5945c2be5cbb2b3ed9b2ccb718d0b3d"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 852,
         "digest": "sha256:f9a83bce3af0648efaa60b9bb28225b09136d2d35d0bed25ac764297076dec1b"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 163,
         "digest": "sha256:b6b53be908de2c0c78070fff0a9f04835211b3156c4e73785747af365e71a0d7"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 403170736,
         "digest": "sha256:5650063cfbfb957d6cfca383efa7ad6618337abcd6d99b247d546f94e2ffb7a9"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 81117097,
         "digest": "sha256:89142850430d0d812f21f8bfef65dcfb42efe2cd2f265b46b73f41fa65bef2fe"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 6868,
         "digest": "sha256:498b10157bcd37c3d4d641c370263e7cf0face8df82130ac1185ef6b2f532470"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 144376365,
         "digest": "sha256:a77a3b1caf74cc7c9fb700cab353313f1b95db5299642f82e56597accb419d7c"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 1551901872,
         "digest": "sha256:0603289dda032b5119a43618c40948658a13e954f7fd7839c42f78fd0a2b9e44"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 467065,
         "digest": "sha256:c3ae245b40c1493b89caa2f5e444da5c0b6f225753c09ddc092252bf58e84264"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 324,
         "digest": "sha256:67e85692af8b802b6110c0a039f582f07db8ac6efc23227e54481f690f1afaae"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 450,
         "digest": "sha256:ea72ab3b716788097885d2d537d1d17c9dc6d9911e01699389fa8c9aa6cac861"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 197,
         "digest": "sha256:b02850f0d90ca01b50bbfb779bcf368507c266fc10cc1feeac87c926e9dda2c1"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 198,
         "digest": "sha256:4295de6959cedecdd0ba31406e15c19e38c13c0ebc38f3d6385725501063ef46"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 213,
         "digest": "sha256:d651a7c122d62d2869af2a5330c756f2f4b35a8e44902174be5c8ce1ad105edd"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 213,
         "digest": "sha256:69e0b993e5f56695ee76b3776275dac236d38d32ba1f380fd78b900232e006ec"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 527,
         "digest": "sha256:8acf43af6deded9b9b94673ed38d3d3d9872fdedd472bf0e451d88417eaf0ae7"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 458,
         "digest": "sha256:5d601f20bb54a0bed11ba297aef4489c21a2e32837e9f130d6d463f024e8508f"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 21087567,
         "digest": "sha256:2c6b9023c3f5686d42451263eb25ed97fb001922603901553ea5f988d094c226"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 109592169,
         "digest": "sha256:e54006d42d65b4c558456226f016b0caf85fac010e4d71a87f68f02706d3fb99"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 277958141,
         "digest": "sha256:eb39f886f65e56bb96df359aa840d94af6b864706e647636531569af867cc7e1"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 207937117,
         "digest": "sha256:ad5fbc417d3686516a6fbdde2d576225824607aafb66e8544ee0657b882de26f"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 96474602,
         "digest": "sha256:c5798387a7f3988f70532ac53bcb17bfe34f4beabece04c9ba2eef943f80c007"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 108017870,
         "digest": "sha256:0188d4d85fec77ae50b16ade4c39acc5c50271fa0bc53a9cdd16fa10c5834baf"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 1026762008,
         "digest": "sha256:ab0030579ceffba3c070467fbdc17d2fe08f51eddcc666fd72f95c158282e924"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 74960529,
         "digest": "sha256:ebda90cd053a0918198e84772d2b619f9f900c8cd3bdf8a84854b355ebe15979"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 46048027,
         "digest": "sha256:38f83ca2690438d1b70bcc78720bf6e050356978f25c80a437ff9fe071216a44"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 59099501,
         "digest": "sha256:e0c4332240fa17b76c6e565e6043600e1afbc16a60a186e76e5b95317eac766f"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 394267867,
         "digest": "sha256:0f4a4a8482bbe2f5253234871a7049fd0141464cad01167e876283db4f26ac13"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 46394076,
         "digest": "sha256:8c83e945eb7e1542dcd507cf65f906a41894653f9a9735f882032b2d238c426e"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 105259490,
         "digest": "sha256:b46af42920bf0f7bd398b2514a9c950529366a03032676a20c3b67b83f3b98a6"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 890007247,
         "digest": "sha256:fe0daf73df35db2e4dabec705a1be1ee20ecfebbe5269db19b91b4a9eecdfa31"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 179777570,
         "digest": "sha256:ef08328ff91b8a96a4dc38f7b130b58c68ed2a882424dad7902c87db3ec5b7cc"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 10624117,
         "digest": "sha256:4084da320e25f250975d76faa9bc8c5bdce2d0ac5eead0ba3423667b95ef1d97"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 1845171,
         "digest": "sha256:72fc5e0c352dd65f2b1ade2cf7e9bc34847e5c719efd146a64dbfd5f69f9aebb"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 78166067,
         "digest": "sha256:0cdb3e9830dae29323a88b4db4089fd797d8e659937a0b8ae2979365fda04953"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 3265,
         "digest": "sha256:5442e5c89de8e839e740d7191c12f8ddf1424a4c72c18e75fcc44bf29d6aabd3"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 2165,
         "digest": "sha256:08163433fa444e26cffd30815aa9cfc2456e8c5ec68b15c843fea2a04ab5edd9"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 1272,
         "digest": "sha256:e96b7a910617fed31061bf4813048a77032366d2ab1de86db7177d9b4d1787b6"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 645,
         "digest": "sha256:284f292c442a4121bd766ba3dca03c223b33063841cbe1e9a93ca09e862369c3"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 2053,
         "digest": "sha256:fa953461a96e791f9299847540ab3069bc342a40b4c164541137bdccf3e374b6"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 877,
         "digest": "sha256:fbbb138c817f73be6ca8bfc9ad7bb22b69d1adaea242e800eb7ff8b353a1be96"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 382,
         "digest": "sha256:dec7a809f7542dba00f22055ef802b8e6e1eeb3e4ab2b9765da9203fdead4a17"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 213,
         "digest": "sha256:264e29b8793ab9c925fd2cf793e6fc5de4a9ee03fb15d3780626ccf9d9c156ad"
      }
   ]
}

