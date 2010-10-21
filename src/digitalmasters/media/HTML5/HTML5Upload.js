/*function inc(filename)
{
var body = document.getElementsByTagName('body').item(0);
script = document.createElement('script');
script.src = filename;
script.type = 'text/javascript';
body.appendChild(script)
}

inc("/static/genlib_media/resources/prototype.js");*/

var HTML5DropBox = Class.create({
  initialize: function(formName, formAction, containerID) {
        this.dropContainer = $(containerID);
        this.dropListing = this.dropContainer.down();
        this.actionPage = formAction;
        this.maxAllowedByteSize = -1;
        this.acceptedFileTypes = new Array();
        this.clearAllBeforeDrop = false;
        this.formName = formName;
        this.imageWidth = 185;
        this.imageHeight = 100;
        //Below is counter to tell when all files are uploaded. Not used effectively yet....
        this.uploadFileCount = 0;
        
        var self = this;
        
        //HTML5 File API supported?
        if(typeof window["FileReader"] === "function") {
          this.dropContainer.addEventListener("dragenter", function (event){ self.dragenter(event); }, false);
          this.dropContainer.addEventListener("dragover", function(event){event.stopPropagation();event.preventDefault();}, false);
          this.dropContainer.addEventListener("drop", function (event){ self.handleDrop(event); }, false);
  
        } else {
          // No File API support fallback to file input. Currently half-baked and only just displays the upload box in IE.
          var fileUploadString = '<input type="file" name="fileManualUpload" id="fileManualUpload" multiple="true" />'
          this.dropListing.remove();
          this.dropContainer.insert({before:fileUploadString});
          this.dropContainer.remove();
          $('btn_clear').remove();
          //$('fileManualUpload').addEventListener("change", function (event){ self.handleDrop(event); }, false);
        }
        
        },
  
  setActionPage: function(action_page) {
    this.actionPage = action_page;
  },
  
  setAcceptedFileType: function(acceptedType) {
    this.acceptedFileTypes[this.acceptedFileTypes.length] = acceptedType;
  },
  
  setMaxAllowedByteSize: function(acceptedByteSize) {
    //Note: -1 for any size.
    this.maxAllowedByteSize = acceptedByteSize;
  },
  
  setClearAllBeforeDrop: function(value) {
    this.clearAllBeforeDrop = value;
  },
  
  clearAllDisplayed: function() {
    this.dropListing.innerHTML = '';
  },
  
  setImageWidth: function(width) {
    this.imageWidth = width;
  },
  
  setImageHeight: function(height) {
    this.imageHeight = height;
  },
  
  setContainerHeight: function(height) {
    this.dropContainer.style.minHeight = height;
  },
  
  setContainerWidth: function(width) {
    this.dropContainer.style.minWidth = width;
  },
  
  dragenter: function(event) {
    if(this.clearAllBeforeDrop == true)
    {
      this.dropListing.innerHTML = '';
    }
    
    $('btn_ingest').disabled = true;
    event.stopPropagation();
    event.preventDefault();
  },
  
  checkFileType: function(fileType) {
    var splitCurrentFileType = fileType.split("/");

    for(var i=0; i<this.acceptedFileTypes.length;i++)
    {
        var splitCurrentAcceptedType = this.acceptedFileTypes[i].split("/");
        var fileTypeAllowed = true;
        
        //Have to pass */* for all files? The below would not allow a simple "*" or "audio" without the slash.
        if(splitCurrentAcceptedType.length == splitCurrentFileType.length)
        {
          //loop through both sections. Only set flag to false if one section of the "/" doesn't match or isn't a "*".
           for(var j=0;j<splitCurrentAcceptedType.length;j++)
           {
             if(splitCurrentAcceptedType[j] != "*" && splitCurrentAcceptedType[j] != splitCurrentFileType[j])
             {
               fileTypeAllowed = false;
             }
           }  
        }
        else {
          //This is the else to the length check.... set to false since length not equal.
          fileTypeAllowed = false;
        }
        
        //If none of the checks failed for this record, must be a match, so return true. Otherwise, continue to loop.
        if(fileTypeAllowed == true) {
          return true;
        }
    }
    
    return false;
  },
  
  handleDrop: function(event) {
        var dt = event.dataTransfer,
        files = dt.files,
        count = files.length;
        var self = this;
        
        event.stopPropagation();
        event.preventDefault();

        for (var i = 0; i < count; i++) {
          if(files[i].size < this.maxAllowedByteSize || this.maxAllowedByteSize == -1) {
            var file = files[i],
              droppedFileName = file.name,
              reader = new FileReader();
              reader.index = i;
              reader.file = file;
              
              if(this.checkFileType(file.type))
              {
                this.uploadFileCount = this.uploadFileCount + 1;
                reader.onloadend = function (event){ self.buildImageListItem(event); };
                reader.readAsDataURL(file);
              }
              else {
                //handle non correct file here. Better implementation needed than just alert.
                alert('The type "' + file.type + '" is not supported for the file "' + file.name + '"');
              }
          } else {
            //handle max file size here. Better implementation needed than just alert.
            alert('File "' + file.name + '" is too big, needs to be below ' + this.maxAllowedByteSize + ' bytes.');
          }
        }
      },
      
      buildImageListItem: function (event) {
      
        var data = event.target.result,
          index = event.target.index,
          file = event.target.file,
          getBinaryDataReader = new FileReader();
          
        var self = this;
        
        if(file.type.startsWith('image/'))
        {
          srcValue = data // base64 encoded string of local file(s) 
        }
        else if(file.type.startsWith('audio/')) {
          srcValue = "/static/HTML5/music_placeholder.jpg" // placeholder image to represent the audio.
        }
        else {
          srcValue= ''; //Add some other placeholder here.
        }
        //create the insert string values.
        var insertString = '<li id="item' + index + '">';
        insertString = insertString + '<a><img height="' + this.imageHeight + '" width="' + this.imageWidth + '" src="' + srcValue + '" /></a>';
        insertString = insertString + '<p>' + file.name + '</p>';
        insertString = insertString + '</li>';
        
        this.dropListing.insert({bottom:insertString});
        
        getBinaryDataReader.onloadend = function (evt){ self.processXHR(file, index, evt.target.result); };
        
        getBinaryDataReader.readAsBinaryString(file);
      },
      
      processXHR: function (file, index, bin) {
          var xhr = new XMLHttpRequest();
          var container = $("item"+index);
          var fileUpload = xhr.upload;
          
          var progressString = '<div class="progressBar"><p>0%</p></div>'
          
          var self = this;
        
           container.insert({bottom:progressString});
           
           //Currently not implemented.... will implement later...
           /*var deleteXString = '<div class="redX"><img src="/static/genlib_media/resources/redx.jpg" width="20" height="20" /></div>';
           container.insert({bottom:deleteXString});
           Event.observe($(container).down().next().next().next().down(), 'click', this.deleteFileUpload.bindAsEventListener(this), false);
           */
        
        fileUpload.log = container;
        
        fileUpload.addEventListener("progress", function(event) {
          if (event.lengthComputable) {
            var percentage = Math.round((event.loaded * 100) / event.total),
            loaderIndicator = $(container).down().next().next().down();
            if (percentage < 100) {
              loaderIndicator.style.width = (percentage*1) + "px";
              loaderIndicator.textContent = percentage + "%";
            }
          }
        }, false);
        
        fileUpload.addEventListener("load", function(event) {
          container.className = "loaded";
          //console.log("xhr upload of "+container.id+" complete");
        }, false);
        
        
        fileUpload.addEventListener("error", function(event) {
          alert("An error occured uploading a file");
        }, false);
          

        //Here is where we post the file to save file.
        xhr.open("POST", this.actionPage);
        xhr.overrideMimeType('text/plain; charset=x-user-defined-binary');
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        
        //Custom data headers to identify what is being sent.... can add more here. Easiest to see headers in Firefox with firebug.
        xhr.setRequestHeader('X-FILE-NAME', file.name);
        xhr.setRequestHeader('X-FILE-SIZE', file.size);
        xhr.setRequestHeader('X-FILE-TYPE', file.type);
        
        xhr.onreadystatechange = function() {  
          if (xhr.readyState == 4 && xhr.status == 200) {  
             //alert(xhr.responseText.strip()); 
             var hiddenFormString = '<input type="hidden" value="' + xhr.responseText.strip() + '" name="fileUploads" />';
             hiddenFormString = '<input type="hidden" value="' + file.name + '" name="originalFileNames" />';
             container.insert({bottom:hiddenFormString});
             //Below is a temporary way to make sure all files are uploaded before submitting.
             this.uploadFileCount = this.uploadFileCount - 1;
             if(this.uploadFileCount == 0)
             {
              $$('btn_ingest').disabled = false;
             }
          }  
        }
        
        if(XMLHttpRequest.prototype.sendAsBinary) {
          xhr.sendAsBinary(bin);
        }
        else {
          //sendAsBinary is not implemented in Chrome and a simple "send" corrupts the binary data.... but strangley sending the file itself does work in Chrome?
          xhr.setRequestHeader('Content-Type', 'multipart/form-data');
          xhr.send(file);
        }

      },
      
      deleteFileUpload: function (object, index) {
        var container = $("item"+index);
        container.remove();
      }
});
