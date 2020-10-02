#!/usr/bin/env python
# coding: utf-8

# <a id="toc"></a>
# # Table of Contents
# 1. [Introduction](#introduction)
# 1. [Install libraries and packages](#install_libraries_and_packages)
# 1. [Import libraries](#import_libraries)
# 1. [Configure hyper-parameters](#configure_hyper_parameters)
# 1. [Define useful classes](#define_useful_classes)
# 1. [Start the inference process](#start_the_inference_process)
# 1. [Save the submission](#save_the_submission)
# 1. [Conclusion](#conclusion)

# <a id="introduction"></a>
# # Introduction
# 
# So, I have successfully trained a classifier by using a bunch of datasets listed in the [*Other useful datasets*](https://www.kaggle.com/c/deepfake-detection-challenge/discussion/128954) discussion and upload it into Kaggle as an external [*dataset*](https://www.kaggle.com/phunghieu/dfdcmultifacef5-resnet18). Now, let's use this model to infer all videos in the test set then complete this end-to-end solution by submitting the final result to the host :) .
# 
# If you do not know how to train the classifier, please follow this [*link*](https://www.kaggle.com/phunghieu/dfdc-multiface-training).
# 
# ---
# ## Multiface's general diagram
# ![diagram](data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%0A%3C%21DOCTYPE%20svg%20PUBLIC%20%22-%2F%2FW3C%2F%2FDTD%20SVG%201.1%2F%2FEN%22%20%22http%3A%2F%2Fwww.w3.org%2FGraphics%2FSVG%2F1.1%2FDTD%2Fsvg11.dtd%22%3E%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xmlns%3Axlink%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxlink%22%20version%3D%221.1%22%20width%3D%221368%22%20height%3D%22389%22%20viewBox%3D%22-0.5%20-0.5%201368%20389%22%20content%3D%22%26lt%3Bmxfile%20host%3D%26quot%3BElectron%26quot%3B%20modified%3D%26quot%3B2020-02-16T02%3A32%3A31.746Z%26quot%3B%20agent%3D%26quot%3BMozilla%2F5.0%20%28X11%3B%20Linux%20x86_64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20draw.io%2F12.2.2%20Chrome%2F78.0.3904.94%20Electron%2F7.1.0%20Safari%2F537.36%26quot%3B%20etag%3D%26quot%3B8-_NGCFXhlIKuX6CvSf-%26quot%3B%20version%3D%26quot%3B12.2.2%26quot%3B%20type%3D%26quot%3Bdevice%26quot%3B%20pages%3D%26quot%3B1%26quot%3B%26gt%3B%26lt%3Bdiagram%20id%3D%26quot%3BxoFWK3179xdSsBTeCwkt%26quot%3B%20name%3D%26quot%3BPage-1%26quot%3B%26gt%3B7Vpdc%2BMmFP01nmkfNqNvK4%2BJ7aQzm2Q79U67feoQCUvUSKgIxXZ%2FfUEC6wPFlmftKJPuU%2BAIELr3nHsvOBN7lmzvKcjiRxJCPLGMcDux5xPLMs2pzf8IZFchnu1WQERRKAfVwBL9CyVoSLRAIcxbAxkhmKGsDQYkTWHAWhiglGzaw1YEt9%2BagQhqwDIAWEf%2FQCGLK9R3jRr%2FBaIoVm82DfkkAWqwBPIYhGTTgOzFxJ5RQljVSrYziIXxlF2qeXevPN1vjMKUDZngzz%2FfP4Tr2eqfhXn%2FFYLZI%2Fjrk1wlZzv1wTDk3y%2B7hLKYRCQFeFGjt5QUaQjFqgbv1WMeCMk4aHLwb8jYTjoTFIxwKGYJlk%2FhFrFvjfafYqkrV%2FbmW7ly2dmpTsro7luz05gluvW0sqfmVd8nPupVsykbkIIG8ICtLEk%2FQCPIDtm09i6XBSQJ5BviEynEgKGX9kaA5Ge0H1e7kDekF0%2FwqNzlC8CFfNMd4J9lGXPIuEAInVge5tu%2FfRatSLR%2Bevw6e3r6WaNC29GbGDG4zEBpow1Xe9up8rWQMrg9bGrdMnKCo7QjY4U5lf1NrTxTySluqM4zLmRM94c8BsvDGygPf0x1eJo6fuf5hfRo4irJHF0S%2FBU888A3kYPfUYOvq8HvEYNzKTFMf4hhsBj8gWKwxhSDr6cKChJebY3J%2Bj1%2F3wvt1cJvzPs9h6%2BmbovGR0icc86xG1H5ciAlKVTYHRLfLWeEakSAQZ6joALlEPO8WlCl%2FHEx2GOqQW2zUzmNqwavWxKNrQbTH1UN5mkRPSjoS%2FneZipR%2BWJIKjmjDKzpUBm8QonBMpBTfyWI77EOrFabSpbntpeoNiZnNQ%2BS3YU6Edru7qUyhbZQybf993wHBa%2FHLEROYc9ZaDsKBb%2B3LhnKHGGLt%2BSO2nMjyP%2B2uHnQCMUjNmv7P2eUrOGMYH6C3ifWFU%2BYHQhgFKUisXLvQI7fiviPAoBv5IMEhSF%2BLXu0aXqGBNI5RFg9%2BcPpyR%2FWpfKH1XM%2FcfN58b9xgO2M7ABn1Cu%2FdvScHg6f76%2BUteyhAdQZs5RV22yITHP6kdoV5Fl1nb5CW%2BH4sxSzZicYXQ%2FTwsWK2cpLh%2B2UxyATzaB4HlDyP1dCeXjeAyBYR6V8vhQMI8HhEg8BXX%2FhyyBWsv3KcNugVaLnulj1jhve6zH8xe5VLfd9ErRTItvG2ATV7yvfhZ3sjp3Mke1kO2MmtVPuJls5rc5YzbRmttOaTHx1ThvtXDpuTptqUpiV5lshXuXp9%2FdzCDM%2B%2FAkWFOCywTaErsf%2FlUs7h%2FcEY7NPPReLxkrNDdMuQZJxA33YqtxzO05w3EER7GJlua2XbEvGa4eP6wJXmfzEZHu5k5F%2BNNWsX1eDFO9uKXeQCJnHokZtu6rHeLwkwuKfxH3ueQh9fTyqvOlP545O6JR3V71X6h%2BG1FPzeGXknofUvFv%2F81B1P1b%2FC5a9%2BA8%3D%26lt%3B%2Fdiagram%26gt%3B%26lt%3B%2Fmxfile%26gt%3B%22%20style%3D%22background-color%3A%20rgb%28255%2C%20255%2C%20255%29%3B%22%3E%3Cdefs%3E%3Cfilter%20id%3D%22dropShadow%22%3E%3CfeGaussianBlur%20in%3D%22SourceAlpha%22%20stdDeviation%3D%221.7%22%20result%3D%22blur%22%2F%3E%3CfeOffset%20in%3D%22blur%22%20dx%3D%223%22%20dy%3D%223%22%20result%3D%22offsetBlur%22%2F%3E%3CfeFlood%20flood-color%3D%22%233D4574%22%20flood-opacity%3D%220.4%22%20result%3D%22offsetColor%22%2F%3E%3CfeComposite%20in%3D%22offsetColor%22%20in2%3D%22offsetBlur%22%20operator%3D%22in%22%20result%3D%22offsetBlur%22%2F%3E%3CfeBlend%20in%3D%22SourceGraphic%22%20in2%3D%22offsetBlur%22%2F%3E%3C%2Ffilter%3E%3C%2Fdefs%3E%3Cg%20filter%3D%22url%28%23dropShadow%29%22%3E%3Cpath%20d%3D%22M%20880.67%2060%20L%201027.93%2060%22%20fill%3D%22none%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22stroke%22%2F%3E%3Cpath%20d%3D%22M%201038.43%2060%20L%201024.43%2067%20L%201027.93%2060%20L%201024.43%2053%20Z%22%20fill%3D%22%23000000%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22all%22%2F%3E%3Crect%20x%3D%22640%22%20y%3D%220%22%20width%3D%22240%22%20height%3D%22120%22%20fill%3D%22%23ffffff%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20pointer-events%3D%22all%22%2F%3E%3Cg%20transform%3D%22translate%28683.5%2C33.5%29scale%282%29%22%3E%3Cswitch%3E%3CforeignObject%20style%3D%22overflow%3Avisible%3B%22%20pointer-events%3D%22all%22%20width%3D%2276%22%20height%3D%2226%22%20requiredFeatures%3D%22http%3A%2F%2Fwww.w3.org%2FTR%2FSVG11%2Ffeature%23Extensibility%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3A%20inline-block%3B%20font-size%3A%2012px%3B%20font-family%3A%20Helvetica%3B%20color%3A%20rgb%280%2C%200%2C%200%29%3B%20line-height%3A%201.2%3B%20vertical-align%3A%20top%3B%20width%3A%2076px%3B%20white-space%3A%20nowrap%3B%20overflow-wrap%3A%20normal%3B%20text-align%3A%20center%3B%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3Ainline-block%3Btext-align%3Ainherit%3Btext-decoration%3Ainherit%3Bwhite-space%3Anormal%3B%22%3EFace%20Detector%3Cbr%20%2F%3E%28MTCNN%29%3C%2Fdiv%3E%3C%2Fdiv%3E%3C%2FforeignObject%3E%3Ctext%20x%3D%2238%22%20y%3D%2219%22%20fill%3D%22%23000000%22%20text-anchor%3D%22middle%22%20font-size%3D%2212px%22%20font-family%3D%22Helvetica%22%3EFace%20Detector%26lt%3Bbr%26gt%3B%28MTCNN%29%3C%2Ftext%3E%3C%2Fswitch%3E%3C%2Fg%3E%3Cpath%20d%3D%22M%20160.67%2060%20L%20307.93%2060%22%20fill%3D%22none%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22stroke%22%2F%3E%3Cpath%20d%3D%22M%20318.43%2060%20L%20304.43%2067%20L%20307.93%2060%20L%20304.43%2053%20Z%22%20fill%3D%22%23000000%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22all%22%2F%3E%3Cellipse%20cx%3D%2280%22%20cy%3D%2260%22%20rx%3D%2280%22%20ry%3D%2240%22%20fill%3D%22%23ffffff%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20pointer-events%3D%22all%22%2F%3E%3Cg%20transform%3D%22translate%2845.5%2C33.5%29scale%282%29%22%3E%3Cswitch%3E%3CforeignObject%20style%3D%22overflow%3Avisible%3B%22%20pointer-events%3D%22all%22%20width%3D%2234%22%20height%3D%2226%22%20requiredFeatures%3D%22http%3A%2F%2Fwww.w3.org%2FTR%2FSVG11%2Ffeature%23Extensibility%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3A%20inline-block%3B%20font-size%3A%2012px%3B%20font-family%3A%20Helvetica%3B%20color%3A%20rgb%280%2C%200%2C%200%29%3B%20line-height%3A%201.2%3B%20vertical-align%3A%20top%3B%20width%3A%2036px%3B%20white-space%3A%20nowrap%3B%20overflow-wrap%3A%20normal%3B%20text-align%3A%20center%3B%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3Ainline-block%3Btext-align%3Ainherit%3Btext-decoration%3Ainherit%3Bwhite-space%3Anormal%3B%22%3EVideo%3Cbr%20%2F%3E%28.mp4%29%3C%2Fdiv%3E%3C%2Fdiv%3E%3C%2FforeignObject%3E%3Ctext%20x%3D%2217%22%20y%3D%2219%22%20fill%3D%22%23000000%22%20text-anchor%3D%22middle%22%20font-size%3D%2212px%22%20font-family%3D%22Helvetica%22%3E%5BNot%20supported%20by%20viewer%5D%3C%2Ftext%3E%3C%2Fswitch%3E%3C%2Fg%3E%3Cpath%20d%3D%22M%20480.67%2060%20L%20627.93%2060%22%20fill%3D%22none%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22stroke%22%2F%3E%3Cpath%20d%3D%22M%20638.43%2060%20L%20624.43%2067%20L%20627.93%2060%20L%20624.43%2053%20Z%22%20fill%3D%22%23000000%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22all%22%2F%3E%3Cellipse%20cx%3D%22400%22%20cy%3D%2260%22%20rx%3D%2280%22%20ry%3D%2240%22%20fill%3D%22%23ffffff%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20pointer-events%3D%22all%22%2F%3E%3Cg%20transform%3D%22translate%28359.5%2C47.5%29scale%282%29%22%3E%3Cswitch%3E%3CforeignObject%20style%3D%22overflow%3Avisible%3B%22%20pointer-events%3D%22all%22%20width%3D%2240%22%20height%3D%2212%22%20requiredFeatures%3D%22http%3A%2F%2Fwww.w3.org%2FTR%2FSVG11%2Ffeature%23Extensibility%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3A%20inline-block%3B%20font-size%3A%2012px%3B%20font-family%3A%20Helvetica%3B%20color%3A%20rgb%280%2C%200%2C%200%29%3B%20line-height%3A%201.2%3B%20vertical-align%3A%20top%3B%20width%3A%2042px%3B%20white-space%3A%20nowrap%3B%20overflow-wrap%3A%20normal%3B%20text-align%3A%20center%3B%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3Ainline-block%3Btext-align%3Ainherit%3Btext-decoration%3Ainherit%3Bwhite-space%3Anormal%3B%22%3EFrames%3C%2Fdiv%3E%3C%2Fdiv%3E%3C%2FforeignObject%3E%3Ctext%20x%3D%2220%22%20y%3D%2212%22%20fill%3D%22%23000000%22%20text-anchor%3D%22middle%22%20font-size%3D%2212px%22%20font-family%3D%22Helvetica%22%3EFrames%3C%2Ftext%3E%3C%2Fswitch%3E%3C%2Fg%3E%3Cpath%20d%3D%22M%201120%20100%20L%201120.67%20170%20L%201120.67%20227.26%22%20fill%3D%22none%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22stroke%22%2F%3E%3Cpath%20d%3D%22M%201120.67%20237.76%20L%201113.67%20223.76%20L%201120.67%20227.26%20L%201127.67%20223.76%20Z%22%20fill%3D%22%23000000%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22all%22%2F%3E%3Cellipse%20cx%3D%221120%22%20cy%3D%2260%22%20rx%3D%2280%22%20ry%3D%2240%22%20fill%3D%22%23ffffff%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20pointer-events%3D%22all%22%2F%3E%3Cg%20transform%3D%22translate%281087.5%2C47.5%29scale%282%29%22%3E%3Cswitch%3E%3CforeignObject%20style%3D%22overflow%3Avisible%3B%22%20pointer-events%3D%22all%22%20width%3D%2232%22%20height%3D%2212%22%20requiredFeatures%3D%22http%3A%2F%2Fwww.w3.org%2FTR%2FSVG11%2Ffeature%23Extensibility%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3A%20inline-block%3B%20font-size%3A%2012px%3B%20font-family%3A%20Helvetica%3B%20color%3A%20rgb%280%2C%200%2C%200%29%3B%20line-height%3A%201.2%3B%20vertical-align%3A%20top%3B%20width%3A%2034px%3B%20white-space%3A%20nowrap%3B%20overflow-wrap%3A%20normal%3B%20text-align%3A%20center%3B%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3Ainline-block%3Btext-align%3Ainherit%3Btext-decoration%3Ainherit%3Bwhite-space%3Anormal%3B%22%3EFaces%3C%2Fdiv%3E%3C%2Fdiv%3E%3C%2FforeignObject%3E%3Ctext%20x%3D%2216%22%20y%3D%2212%22%20fill%3D%22%23000000%22%20text-anchor%3D%22middle%22%20font-size%3D%2212px%22%20font-family%3D%22Helvetica%22%3EFaces%3C%2Ftext%3E%3C%2Fswitch%3E%3C%2Fg%3E%3Cpath%20d%3D%22M%20280.67%20300%20Q%20180.67%20300%20180.67%20270%20Q%20180.67%20240%2093.4%20240%22%20fill%3D%22none%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22stroke%22%2F%3E%3Cpath%20d%3D%22M%2082.9%20240%20L%2096.9%20233%20L%2093.4%20240%20L%2096.9%20247%20Z%22%20fill%3D%22%23000000%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22all%22%2F%3E%3Cpath%20d%3D%22M%20280.67%20300%20Q%20180.67%20300%20180.67%20330%20Q%20180.67%20360%2093.4%20360%22%20fill%3D%22none%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22stroke%22%2F%3E%3Cpath%20d%3D%22M%2082.9%20360%20L%2096.9%20353%20L%2093.4%20360%20L%2096.9%20367%20Z%22%20fill%3D%22%23000000%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22all%22%2F%3E%3Crect%20x%3D%220%22%20y%3D%22220%22%20width%3D%2280%22%20height%3D%2240%22%20fill%3D%22none%22%20stroke%3D%22none%22%20pointer-events%3D%22all%22%2F%3E%3Cg%20transform%3D%22translate%287.5%2C227.5%29scale%282%29%22%3E%3Cswitch%3E%3CforeignObject%20style%3D%22overflow%3Avisible%3B%22%20pointer-events%3D%22all%22%20width%3D%2232%22%20height%3D%2212%22%20requiredFeatures%3D%22http%3A%2F%2Fwww.w3.org%2FTR%2FSVG11%2Ffeature%23Extensibility%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3A%20inline-block%3B%20font-size%3A%2012px%3B%20font-family%3A%20Helvetica%3B%20color%3A%20rgb%280%2C%200%2C%200%29%3B%20line-height%3A%201.2%3B%20vertical-align%3A%20top%3B%20width%3A%2032px%3B%20white-space%3A%20nowrap%3B%20overflow-wrap%3A%20normal%3B%20text-align%3A%20center%3B%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3Ainline-block%3Btext-align%3Ainherit%3Btext-decoration%3Ainherit%3Bwhite-space%3Anormal%3B%22%3EREAL%3C%2Fdiv%3E%3C%2Fdiv%3E%3C%2FforeignObject%3E%3Ctext%20x%3D%2216%22%20y%3D%2212%22%20fill%3D%22%23000000%22%20text-anchor%3D%22middle%22%20font-size%3D%2212px%22%20font-family%3D%22Helvetica%22%3EREAL%3C%2Ftext%3E%3C%2Fswitch%3E%3C%2Fg%3E%3Crect%20x%3D%220%22%20y%3D%22340%22%20width%3D%2280%22%20height%3D%2240%22%20fill%3D%22none%22%20stroke%3D%22none%22%20pointer-events%3D%22all%22%2F%3E%3Cg%20transform%3D%22translate%289.5%2C347.5%29scale%282%29%22%3E%3Cswitch%3E%3CforeignObject%20style%3D%22overflow%3Avisible%3B%22%20pointer-events%3D%22all%22%20width%3D%2230%22%20height%3D%2212%22%20requiredFeatures%3D%22http%3A%2F%2Fwww.w3.org%2FTR%2FSVG11%2Ffeature%23Extensibility%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3A%20inline-block%3B%20font-size%3A%2012px%3B%20font-family%3A%20Helvetica%3B%20color%3A%20rgb%280%2C%200%2C%200%29%3B%20line-height%3A%201.2%3B%20vertical-align%3A%20top%3B%20width%3A%2032px%3B%20white-space%3A%20nowrap%3B%20overflow-wrap%3A%20normal%3B%20text-align%3A%20center%3B%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3Ainline-block%3Btext-align%3Ainherit%3Btext-decoration%3Ainherit%3Bwhite-space%3Anormal%3B%22%3EFAKE%3C%2Fdiv%3E%3C%2Fdiv%3E%3C%2FforeignObject%3E%3Ctext%20x%3D%2215%22%20y%3D%2212%22%20fill%3D%22%23000000%22%20text-anchor%3D%22middle%22%20font-size%3D%2212px%22%20font-family%3D%22Helvetica%22%3EFAKE%3C%2Ftext%3E%3C%2Fswitch%3E%3C%2Fg%3E%3Cpath%20d%3D%22M%201060.67%20300%20L%20892.74%20300%22%20fill%3D%22none%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22stroke%22%2F%3E%3Cpath%20d%3D%22M%20882.24%20300%20L%20896.24%20293%20L%20892.74%20300%20L%20896.24%20307%20Z%22%20fill%3D%22%23000000%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22all%22%2F%3E%3Crect%20x%3D%221060%22%20y%3D%22240%22%20width%3D%2280%22%20height%3D%2280%22%20fill%3D%22%23ffffff%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20pointer-events%3D%22all%22%2F%3E%3Cpath%20d%3D%22M%20760%20240%20L%20840%20240%20L%20880%20280%20L%20880%20360%20L%20800%20360%20L%20760%20320%20L%20760%20240%20Z%22%20fill%3D%22%23ffffff%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22all%22%2F%3E%3Cpath%20d%3D%22M%20760%20240%20L%20840%20240%20L%20880%20280%20L%20800%20280%20Z%22%20fill-opacity%3D%220.05%22%20fill%3D%22%23000000%22%20stroke%3D%22none%22%20pointer-events%3D%22all%22%2F%3E%3Cpath%20d%3D%22M%20760%20240%20L%20800%20280%20L%20800%20360%20L%20760%20320%20Z%22%20fill-opacity%3D%220.1%22%20fill%3D%22%23000000%22%20stroke%3D%22none%22%20pointer-events%3D%22all%22%2F%3E%3Cpath%20d%3D%22M%20800%20360%20L%20800%20280%20L%20760%20240%20M%20800%20280%20L%20880%20280%22%20fill%3D%22none%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22all%22%2F%3E%3Crect%20x%3D%221080%22%20y%3D%22260%22%20width%3D%2280%22%20height%3D%2280%22%20fill%3D%22%23ffffff%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20pointer-events%3D%22all%22%2F%3E%3Crect%20x%3D%221100%22%20y%3D%22280%22%20width%3D%2280%22%20height%3D%2280%22%20fill%3D%22%23ffffff%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20pointer-events%3D%22all%22%2F%3E%3Cpath%20d%3D%22M%20573.4%20300%20L%20760%20300%22%20fill%3D%22none%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22stroke%22%2F%3E%3Cpath%20d%3D%22M%20562.9%20300%20L%20576.9%20293%20L%20573.4%20300%20L%20576.9%20307%20Z%22%20fill%3D%22%23000000%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20pointer-events%3D%22all%22%2F%3E%3Crect%20x%3D%22280%22%20y%3D%22240%22%20width%3D%22280%22%20height%3D%22120%22%20fill%3D%22%23ffffff%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20pointer-events%3D%22all%22%2F%3E%3Cg%20transform%3D%22translate%28297.5%2C273.5%29scale%282%29%22%3E%3Cswitch%3E%3CforeignObject%20style%3D%22overflow%3Avisible%3B%22%20pointer-events%3D%22all%22%20width%3D%22122%22%20height%3D%2226%22%20requiredFeatures%3D%22http%3A%2F%2Fwww.w3.org%2FTR%2FSVG11%2Ffeature%23Extensibility%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3A%20inline-block%3B%20font-size%3A%2012px%3B%20font-family%3A%20Helvetica%3B%20color%3A%20rgb%280%2C%200%2C%200%29%3B%20line-height%3A%201.2%3B%20vertical-align%3A%20top%3B%20width%3A%20124px%3B%20white-space%3A%20nowrap%3B%20overflow-wrap%3A%20normal%3B%20text-align%3A%20center%3B%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3Ainline-block%3Btext-align%3Ainherit%3Btext-decoration%3Ainherit%3Bwhite-space%3Anormal%3B%22%3EClassifier%3Cbr%20%2F%3E%28Deep%20Neural%20Network%29%3C%2Fdiv%3E%3C%2Fdiv%3E%3C%2FforeignObject%3E%3Ctext%20x%3D%2261%22%20y%3D%2219%22%20fill%3D%22%23000000%22%20text-anchor%3D%22middle%22%20font-size%3D%2212px%22%20font-family%3D%22Helvetica%22%3EClassifier%26lt%3Bbr%26gt%3B%28Deep%20Neural%20Network%29%3C%2Ftext%3E%3C%2Fswitch%3E%3C%2Fg%3E%3Crect%20x%3D%221140%22%20y%3D%22150%22%20width%3D%2280%22%20height%3D%2240%22%20fill%3D%22none%22%20stroke%3D%22none%22%20pointer-events%3D%22all%22%2F%3E%3Cg%20transform%3D%22translate%281139.5%2C157.5%29scale%282%29%22%3E%3Cswitch%3E%3CforeignObject%20style%3D%22overflow%3Avisible%3B%22%20pointer-events%3D%22all%22%20width%3D%2240%22%20height%3D%2212%22%20requiredFeatures%3D%22http%3A%2F%2Fwww.w3.org%2FTR%2FSVG11%2Ffeature%23Extensibility%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3A%20inline-block%3B%20font-size%3A%2012px%3B%20font-family%3A%20Helvetica%3B%20color%3A%20rgb%280%2C%200%2C%200%29%3B%20line-height%3A%201.2%3B%20vertical-align%3A%20top%3B%20width%3A%2042px%3B%20white-space%3A%20nowrap%3B%20overflow-wrap%3A%20normal%3B%20text-align%3A%20center%3B%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3Ainline-block%3Btext-align%3Ainherit%3Btext-decoration%3Ainherit%3Bwhite-space%3Anormal%3B%22%3ESample%3C%2Fdiv%3E%3C%2Fdiv%3E%3C%2FforeignObject%3E%3Ctext%20x%3D%2220%22%20y%3D%2212%22%20fill%3D%22%23000000%22%20text-anchor%3D%22middle%22%20font-size%3D%2212px%22%20font-family%3D%22Helvetica%22%3ESample%3C%2Ftext%3E%3C%2Fswitch%3E%3C%2Fg%3E%3Crect%20x%3D%22930%22%20y%3D%22260%22%20width%3D%2280%22%20height%3D%2240%22%20fill%3D%22none%22%20stroke%3D%22none%22%20pointer-events%3D%22all%22%2F%3E%3Cg%20transform%3D%22translate%28939.5%2C267.5%29scale%282%29%22%3E%3Cswitch%3E%3CforeignObject%20style%3D%22overflow%3Avisible%3B%22%20pointer-events%3D%22all%22%20width%3D%2230%22%20height%3D%2212%22%20requiredFeatures%3D%22http%3A%2F%2Fwww.w3.org%2FTR%2FSVG11%2Ffeature%23Extensibility%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3A%20inline-block%3B%20font-size%3A%2012px%3B%20font-family%3A%20Helvetica%3B%20color%3A%20rgb%280%2C%200%2C%200%29%3B%20line-height%3A%201.2%3B%20vertical-align%3A%20top%3B%20width%3A%2032px%3B%20white-space%3A%20nowrap%3B%20overflow-wrap%3A%20normal%3B%20text-align%3A%20center%3B%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3Ainline-block%3Btext-align%3Ainherit%3Btext-decoration%3Ainherit%3Bwhite-space%3Anormal%3B%22%3EStack%3C%2Fdiv%3E%3C%2Fdiv%3E%3C%2FforeignObject%3E%3Ctext%20x%3D%2215%22%20y%3D%2212%22%20fill%3D%22%23000000%22%20text-anchor%3D%22middle%22%20font-size%3D%2212px%22%20font-family%3D%22Helvetica%22%3EStack%3C%2Ftext%3E%3C%2Fswitch%3E%3C%2Fg%3E%3Cpath%20d%3D%22M%201260%20240%20L%201250%20240%20Q%201240%20240%201240%20260%20L%201240%20280%20Q%201240%20300%201230%20300%20L%201225%20300%20Q%201220%20300%201230%20300%20L%201235%20300%20Q%201240%20300%201240%20320%20L%201240%20340%20Q%201240%20360%201250%20360%20L%201260%20360%22%20fill%3D%22none%22%20stroke%3D%22%23000000%22%20stroke-width%3D%222%22%20stroke-miterlimit%3D%2210%22%20transform%3D%22rotate%28-180%2C1240%2C300%29%22%20pointer-events%3D%22all%22%2F%3E%3Crect%20x%3D%221260%22%20y%3D%22280%22%20width%3D%22100%22%20height%3D%2240%22%20fill%3D%22none%22%20stroke%3D%22none%22%20pointer-events%3D%22all%22%2F%3E%3Cg%20transform%3D%22translate%281271.5%2C287.5%29scale%282%29%22%3E%3Cswitch%3E%3CforeignObject%20style%3D%22overflow%3Avisible%3B%22%20pointer-events%3D%22all%22%20width%3D%2238%22%20height%3D%2212%22%20requiredFeatures%3D%22http%3A%2F%2Fwww.w3.org%2FTR%2FSVG11%2Ffeature%23Extensibility%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3A%20inline-block%3B%20font-size%3A%2012px%3B%20font-family%3A%20Helvetica%3B%20color%3A%20rgb%280%2C%200%2C%200%29%3B%20line-height%3A%201.2%3B%20vertical-align%3A%20top%3B%20width%3A%2040px%3B%20white-space%3A%20nowrap%3B%20overflow-wrap%3A%20normal%3B%20text-align%3A%20center%3B%22%3E%3Cdiv%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxhtml%22%20style%3D%22display%3Ainline-block%3Btext-align%3Ainherit%3Btext-decoration%3Ainherit%3Bwhite-space%3Anormal%3B%22%3En%20faces%3C%2Fdiv%3E%3C%2Fdiv%3E%3C%2FforeignObject%3E%3Ctext%20x%3D%2219%22%20y%3D%2212%22%20fill%3D%22%23000000%22%20text-anchor%3D%22middle%22%20font-size%3D%2212px%22%20font-family%3D%22Helvetica%22%3En%20faces%3C%2Ftext%3E%3C%2Fswitch%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E)
# 
# ---
# ## Implementation
# I will loop through all test videos and try to get face images by using the same strategy as I have applied to the validation process in the [*DFDC-Multiface-Training*](https://www.kaggle.com/phunghieu/dfdc-multiface-training) kernel. The only difference is instead of having well-prepared data, I must run a face-detector, the same as I used to prepare the training dataset in the [*Data Preparation*](https://www.kaggle.com/phunghieu/deepfake-detection-face-extractor) kernel, to directly extract faces from each frame of one input video.
# 
# If I fail to get enough faces from a video, I will mark it as `invalid` and assign a `default predicted value` (probability) to this video near the end of the notebook.
# 
# ---
# ## Pipeline
# This end-to-end solution includes 3 steps:
# 1. [*Data Preparation*](https://www.kaggle.com/phunghieu/deepfake-detection-face-extractor)
# 1. [*Training*](https://www.kaggle.com/phunghieu/dfdc-multiface-training)
# 1. *Inference* <- **you're here**
# 
# [Back to Table of Contents](#toc)

# <a id="install_libraries_and_packages"></a>
# # Install libraries and packages
# [Back to Table of Contents](#toc)

# In[ ]:


# Install facenet-pytorch
get_ipython().system('pip install /kaggle/input/facenet-pytorch-vggface2/facenet_pytorch-2.0.0-py3-none-any.whl')

from facenet_pytorch.models.inception_resnet_v1 import get_torch_home
torch_home = get_torch_home()

# Copy model checkpoints to torch cache so they are loaded automatically by the package
get_ipython().system('mkdir -p $torch_home/checkpoints/')
get_ipython().system('cp /kaggle/input/facenet-pytorch-vggface2/20180402-114759-vggface2-logits.pth $torch_home/checkpoints/vggface2_DG3kwML46X.pt')
get_ipython().system('cp /kaggle/input/facenet-pytorch-vggface2/20180402-114759-vggface2-features.pth $torch_home/checkpoints/vggface2_G5aNV2VSMn.pt')


# <a id="import_libraries"></a>
# # Import libraries
# [Back to Table of Contents](#toc)

# In[ ]:


import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torchvision.models import resnet18
from facenet_pytorch import MTCNN
from albumentations import Normalize, Compose
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from tqdm.notebook import tqdm
import os
import glob
import multiprocessing as mp

if torch.cuda.is_available():
    device = 'cuda:0'
    torch.set_default_tensor_type('torch.cuda.FloatTensor')
else:
    device = 'cpu'
print(f'Running on device: {device}')


# <a id="configure_hyper_parameters"></a>
# # Configure hyper-parameters
# [Back to Table of Contents](#toc)

# In[ ]:


TEST_DIR = '/kaggle/input/deepfake-detection-challenge/test_videos/'
MODEL_PATH = '/kaggle/input/dfdcmultifacef5-resnet18/f5_resnet18.pth'

N_FACES = 5
BATCH_SIZE = 64
NUM_WORKERS = mp.cpu_count()

FRAME_SCALE = 0.25
FACE_BATCH_SHAPE = (N_FACES*3, 160, 160)

DEFAULT_PROB = 0.5


# <a id="define_useful_classes"></a>
# # Define useful classes
# [Back to Table of Contents](#toc)

# In[ ]:


class DeepfakeClassifier(nn.Module):
    def __init__(self, encoder, in_channels=3, num_classes=1):
        super(DeepfakeClassifier, self).__init__()
        self.encoder = encoder
        
        # Modify input layer.
        self.encoder.conv1 = nn.Conv2d(
            in_channels,
            64,
            kernel_size=7,
            stride=2,
            padding=3,
            bias=False
        )
        
        # Modify output layer.
        self.encoder.fc = nn.Linear(512 * 1, num_classes)

    def forward(self, x):
        return torch.sigmoid(self.encoder(x))
    
    def freeze_all_layers(self):
        for param in self.encoder.parameters():
            param.requires_grad = False

    def freeze_middle_layers(self):
        self.freeze_all_layers()
        
        for param in self.encoder.conv1.parameters():
            param.requires_grad = True
            
        for param in self.encoder.fc.parameters():
            param.requires_grad = True

    def unfreeze_all_layers(self):
        for param in self.encoder.parameters():
            param.requires_grad = True
            
            
class TestVideoDataset(Dataset):
    def __init__(self, test_dir, frame_resize=None, face_detector=None, n_faces=1, preprocess=None):
        self.test_dir = test_dir
        self.test_video_paths = glob.glob(os.path.join(self.test_dir, '*.mp4'))
        self.face_detector = face_detector
        self.n_faces = n_faces
        self.frame_resize = frame_resize
        self.preprocess = preprocess

    def __len__(self):
        return len(self.test_video_paths)
    
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        test_video_path = self.test_video_paths[idx]
        test_video = test_video_path.split('/')[-1]
        
        # Get faces until enough (try limit: n_faces)
        faces = []
        
        for i in range(self.n_faces):
            # Create video reader and find length
            v_cap = cv2.VideoCapture(test_video_path)
            v_len = int(v_cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            stride = int(v_len/(self.n_faces**2))
            sample = np.linspace(i*stride, (v_len - 1) + i*stride, self.n_faces).astype(int)
            frames = []

            # Get frames
            for j in range(v_len):
                success = v_cap.grab()
                
                if j in sample:
                    success, frame = v_cap.retrieve()

                    if not success:
                        continue

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = Image.fromarray(frame)

                    # Resize frame to desired size
                    if self.frame_resize is not None:
                        frame = frame.resize([int(d * self.frame_resize) for d in frame.size])
                    frames.append(frame)
            
            if len(frames) > 0:
                all_faces_in_frames = [
                    detected_face
                    for detected_faces in self.face_detector(frames)
                    if detected_faces is not None
                    for detected_face in detected_faces
                ]

                faces.extend(all_faces_in_frames)
            
            if len(faces) >= self.n_faces: # Get enough faces
                break

        v_cap.release()

        if len(faces) >= self.n_faces: # Get enough faces
            faces = faces[:self.n_faces] # Get top
            
            if self.preprocess is not None:
                for j in range(len(faces)):
                    augmented = self.preprocess(image=faces[j].cpu().detach().numpy().transpose(1, 2, 0))
                    faces[j] = augmented['image']
            
            faces = np.concatenate(faces, axis=-1).transpose(2, 0, 1)
            
            return {
                'video_name': test_video,
                'faces': faces,
                'is_valid': True
            }
        else:
            return {
                'video_name': test_video,
                'faces': np.zeros(FACE_BATCH_SHAPE, dtype=np.float32),
                'is_valid': False # Those invalid videos will get DEFAULT_PROB
            }


# <a id="start_the_inference_process"></a>
# # Start the inference process
# [Back to Table of Contents](#toc)

# In[ ]:


# Load face detector.
face_detector = MTCNN(margin=14, keep_all=True, factor=0.5, post_process=False, device=device).eval()


# In[ ]:


encoder = resnet18(pretrained=False)

classifier = DeepfakeClassifier(encoder=encoder, in_channels=3*N_FACES, num_classes=1)
classifier.to(device)
state = torch.load(MODEL_PATH, map_location=lambda storage, loc: storage)
classifier.load_state_dict(state['state_dict'])
classifier.eval()


# In[ ]:


preprocess = Compose([
    Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225], p=1)
])


# In[ ]:


test_dataset = TestVideoDataset(
    TEST_DIR,
    frame_resize=FRAME_SCALE,
    face_detector=face_detector,
    n_faces=N_FACES,
    preprocess=preprocess
)

test_dataloader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS
)


# In[ ]:


submission = []

with torch.no_grad():
    try:
        for videos in tqdm(test_dataloader):
            y_pred = classifier(videos['faces']).squeeze(dim=-1).cpu().detach().numpy()
            submission.extend(list(zip(videos['video_name'], y_pred, videos['is_valid'].cpu().detach().numpy())))
    except Exception as e:
        print(e)
        
submission = pd.DataFrame(submission, columns=['filename', 'label', 'is_valid'])
submission.sort_values('filename', inplace=True)
submission.loc[submission.is_valid == False, 'label'] = DEFAULT_PROB


# <a id="save_the_submission"></a>
# # Save the submission
# [Back to Table of Contents](#toc)

# In[ ]:


submission[['filename', 'label']].to_csv('submission.csv', index=False)

plt.hist(submission.label, 20)
plt.show()


# <a id="conclusion"></a>
# # Conclusion
# Finally, we made it! Let's submit the result to see whether we can get a better position in the Public Leaderboard =]]
# 
# If you have any questions or suggestions, feel free to move to the `comments` section below.
# 
# ---
# The content in this notebook is too complicated to understand and you want a simpler solution to get started, I have already prepared one for you based on `@timesler`'s solution in this series:
# * [Deepfake Detection - Data Preparation (baseline)](https://www.kaggle.com/phunghieu/deepfake-detection-data-preparation-baseline)
# * [Deepfake Detection - Training (baseline)](https://www.kaggle.com/phunghieu/deepfake-detection-training-baseline)
# * [Deepfake Detection - Inference (baseline)](https://www.kaggle.com/phunghieu/deepfake-detection-inference-baseline)
# 
# ---
# Please upvote this kernel if you think it is worth reading.
# 
# Thank you so much!
# 
# [Back to Table of Contents](#toc)
