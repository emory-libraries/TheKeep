/**
HTML5 drag & drop uploader with client-side MD5 checksum.

Should be initialized with a url parameter and optionally a list of allowed
mimetypes.  For example:

<script type="text/javascript" charset="utf-8">
   $("#drop_target").md5DropUploader({
      url : "{% url audio:upload %}",
      allowed_types : ['audio/wav', 'audio/mp3'],
   });
</script>

When files are dropped on the specified element, files will be checked to
see if they are in the list of allowed types (when specified), an MD5 checksum
will be calculated on the client side, and then the file will be posted
the the configured url.  On successful upload, hidden form inputs will be added
with the original file name, the response from the ajax POST request (assumed
here to be an upload id), and the client-side calculated MD5 checksum.

File uploads are POSTed to the configured url with these HTTP headers:

  Content-Disposition:  filename=original_file.ext
  Content-Type
  Content-MD5

Adapted in part from https://github.com/texel/drag_drop_example/

*/

(function( $ ){

  var methods = {
    init : function(options) {  

    return this.each(function(){
    /* initialize the object:
        configure settings, add special upload & submit button, and
        bind methods as event handlers.
    */
       var $this = $(this);
       var data = {
        'file_count': 0,
        'files': new Array(),
        'ingest_on_completion': false,
        allowed_types: [],
       };
       $.extend(data, options);

       // TODO: consolidate submission/wait-for-upload logic in a single
       // form submission button
       // create a special-function ingest button and add it after uploader element
       var ingest_button = $('<input type="button" value="Submit when all uploads complete"/>');
       $this.after(ingest_button);
       // place-holder for submit information
       ingest_button.after('<p id="upload-submit-info"/>');
       ingest_button.click(function(){
          // set a flag to automatically ingest when upload completes for all files
          var data = $(this).prev().data('md5DropUploader');
          data['ingest_on_completion'] = true;
          $(this).prev().data('md5DropUploader', data);
          $(this).nextAll('#upload-submit-info').html("Items will be submitted for ingest when all uploads complete.");
       });

       // following recommended practice: store data in one object with name of plugin
       $this.data('md5DropUploader', data);

       $this.bind('dragenter.md5DropUploader', methods.dragEnter);
       $this.bind('dragover.md5DropUploader', methods.dragOver);
       $this.bind('drop.md5DropUploader', methods.drop);
       $this.bind('dragleave.md5DropUploader', methods.dragLeave);
       // custom event to be triggered after a file is uploaded
       $this.bind('afterUpload.md5DropUploader', methods.afterUpload);
     });
    },

    dragEnter : function (event) {
      $(this).addClass('dragover');
      event.stopPropagation();
      event.preventDefault();

      return false;
    },

    dragOver : function (event) {
      $(this).addClass('dragover');
      event.stopPropagation();
      event.preventDefault();

      return false;
    },

    dragLeave : function (event) {
      $(this).removeClass('dragover');

      return false;
    },

    drop : function(event) {
    /* Process files that are dropped.  Add any allowed types to the stored
       list of files, then MD5 sum and upload each of them, reporting
       status and progress to the user.
    */
      var $this = $(this);
      $this.removeClass('dragover');
      event.stopPropagation();
      event.preventDefault();

      var data = $this.data('md5DropUploader');
      // store current file count - marker for where to start processing in full list of files
      var start_processing = data['file_count'];
      var allowed_types =  data['allowed_types'];
      var not_allowed = new Array();
      // display files if they are allowed type, add to list of all files
      if (event.originalEvent.dataTransfer.files.length > 0) {
        $.each(event.originalEvent.dataTransfer.files, function ( i, file ) {
            // if allowed types have been specified, check that file is one of the specified types
            if (allowed_types.length == 0 ||
                $.inArray(file.type, allowed_types) != -1) {    // returns index or -1 if not found
                // rudimentary list display
                var p = $('<p><a class="remove">X</a> ' + file.fileName + ' ' +
                    '<span class="file-info">(' + filesize_format(file.size) +
		    ', ' + file.type + ')</span></p>');
                $this.append(p);
                // create status node and attach to file so it is easy to update
                file.status = $('<span class="status">-</span>');
                p.append(file.status);
                data['files'].push(file);
                data['file_count']++;
            } else {
                // push dis-allowed files into a list so they can be reported all at once
                not_allowed.push(file);
            }
        });
        // TODO: support abort on checksum/upload if user removes file while processing
        $this.find(".remove").click(function () {$(this).parent().remove(); });

        // report any files that were not in the allowed types
        if (not_allowed.length) {
          var msg = "The following file(s) were not added because the " +
                "type indicates they are not a supported upload formats:\n\n";
          $.each(not_allowed, function ( i, file ) {
            msg += "  " + file.fileName + "\t" + file.type + "\n";
          });
          alert(msg);
        }
        // update stored data with count & list of files
        $this.data('md5DropUploader', data);
	// if there are new files to process, disable submit button until upload completes
        if (data['file_count'] > start_processing) {
          $this.md5DropUploader('disableSubmit');
        }

       // handle files added on the current drop
       // calculate checksum and then upload
       $.each(data['files'], function(i, file) {
            // only process files added on the current drop
            if (i >= start_processing) { 
                // update status
                file.status.html('calculating checksum');
                // give each file a separate reader so they don't clobber each other
                reader = new FileReader();
                // set handler for when file reading completes
                reader.onloadend = function (evt){
                      file.status.html('calculating checksum');
                      file.md5 = rstr2hex(rstr_md5(evt.target.result));
                      console.log(file.fileName + ' checksum ' + file.md5);
                      file.status.html('uploading');
                      $this.md5DropUploader('uploadFile', file);
                    };
                // display checksum progress (currently displays file read progress)
                // TODO: consolidate progress bar logic (duplicated in uploadFile method)
                var indicator = $('<p/>');
                file.progress = $('<div class="progress-bar"/>');
                file.progress.append(indicator);
                file.status.append(file.progress);
                reader.onprogress = function(event) {
                      if (event.lengthComputable) {
                        var percentage = Math.round((event.loaded * 100) / event.total);
                        indicator.width(percentage);
                        indicator.html(percentage + "%");
                      }
                };
                reader.readAsBinaryString(file);
            }
         });
      };
      return false;
    },  // end drop method

    afterUpload: function(event) {
    /**  After each file finishes uploading:
         - check if all files have finished uploading
         - if form submission has been requested after upload completes, submit
           the form
         - otherwise, re-enable the form submit button
    */
        var data = $(this).data('md5DropUploader');
        // check if all files have finished uploaded
        for (var x = 0; x < data['files'].length; x++) {
            if (! data['files'][x].upload_id) {
                return;
            }
        }
        // all files have completed uploading - if requested, submit the form
        if (data['ingest_on_completion']) {
            $(this).parents('form').submit();
            // TODO: may want to display some kind of indicator here...
        }
        // otherwise, re-enable normal submit button
        $(this).md5DropUploader('enableSubmit');
    },

    disableSubmit: function() {
    /* shortcut to disable the form submission button */
       $(this).nextAll('[type="submit"]').attr('disabled', 'disabled');
    },

    enableSubmit: function() {
   /* shortcut to enable the form submission button */
      $(this).nextAll('[type="submit"]').removeAttr('disabled');
    },

    uploadFile: function(file) {
    /*  Upload a file to the configured url via XMLHttpRequest.
        When the request returns status 200, adds hidden form inputs.
        On any other status code, sets file.upload_id to -1 to indicate
        upload completed but did not succeed.
        Triggers custom 'afterUpload' event after the request completes.
    */
        var $this = $(this);
        var data = $this.data('md5DropUploader');
        var xhr   = new XMLHttpRequest();

        // display an upload progress bar
        var indicator = $('<p/>');
        file.progress = $('<div class="progress-bar"/>');
        file.progress.append(indicator);
        file.status.append(file.progress);
        xhr.upload.addEventListener("progress", function(event) {
              if (event.lengthComputable) {
                var percentage = Math.round((event.loaded * 100) / event.total);
                indicator.width(percentage);
                indicator.html(percentage + "%");
              }
            }, false);

        xhr.open('POST', data['url'], true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        // set required headers for processing the file
        xhr.setRequestHeader('Content-Disposition', "filename=" + file.fileName);
        xhr.setRequestHeader('Content-Type', file.type);
        xhr.setRequestHeader('Content-MD5', file.md5);

        // Content-Length header could be set explicitly from file.size,
        // but should be set automatically by the browser (tested in FF and Chrome)

        xhr.onreadystatechange = function() {
          if (xhr.readyState == 4) {
            if(xhr.status == 200) { // ok
                file.status.html('Ready to ingest');
                file.upload_id = xhr.responseText;
                // add form data for submission
                // - adding to file dom element so we can easily remove individual files
                file.status.parent().append('<input type="hidden" name="fileUploads" value="' + file.upload_id + '"/>');
                file.status.parent().append('<input type="hidden" name="originalFileNames" value="' + file.fileName + '"/>');
                file.status.parent().append('<input type="hidden" name="fileMD5sum" value="' + file.md5 + '"/>');

             } else { // if(xhr.status == 400)  // bad request
                file.status.html('Upload error: ' + xhr.responseText);
                file.upload_id = -1;
                // TODO: include upload errors in the form somehow so that
                // we can report them on the form submission page
             }

             // signal the uploader for after-upload logic
             $this.trigger('afterUpload.md5DropUploader');
          }
        };

        xhr.send(file);
    },  // end uploadFile method
  };
  

  $.fn.md5DropUploader = function( method ) {
    if ( methods[method] ) {
      return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
    } else if ( typeof method === 'object' || ! method ) {
      return methods.init.apply( this, arguments );
    } else {
      $.error( 'Method ' +  method + ' does not exist on jQuery.md5DropUploader' );
    }
  };
})( jQuery );



// FIXME: where should filesize_format function go?
/* convert integer filesize in bytes to a human-readable format */
function filesize_format(size) {
    if (size === 0) {
        return '';
    } else if (size < 100) {
        return '' + size + ' bytes';
    } else if (size < (1000 * 1000)) {
        size = size / 1000;
        size = '' + size;
        vals = size.split('.');
        return vals[0] + '.' + vals[1].substring(0, 1) + 'kb';
    } else {
        size = size / (1000 * 1000);
        size = '' + size;
        vals = size.split('.');
        return vals[0] + '.' + vals[1].substring(0, 1) + 'mb';
    }
    // TODO: gb ?
}

