/**
HTML5 drag & drop uploader with client-side MD5 checksum.

Should be initialized with a url parameter and optionally a list of allowed
mimetypes.  For example:

<script type="text/javascript" charset="utf-8">
   $("#drop_target").md5DropUploader({
      url : "{% url audio:upload %}",
      allowed_types : ['audio/wav', 'audio/mp3'],
      csrf_token: "...."
   });
</script>

To avoid having to make your upload views csrf exempt, you
should specify a csrf token.  E.g., include the token on the template using
{% csrf_token %} and then pass via $('input[name="csrfmiddlewaretoken"]').val().

NOTE: according to Django docs it would be better to use the csrf cookie here;
see https://docs.djangoproject.com/en/1.5/ref/contrib/csrf/#ajax

When files are dropped on the specified element, files will be checked to
see if they are in the list of allowed types (when specified), an MD5 checksum
will be calculated on the client side, and then the file will be posted
the the configured url.  On successful upload, hidden form inputs will be added
with the original file name and the response from the ajax POST request (assumed
here to be an upload id).  The md5DropUploader target element should be
 inside a form; this plugin binds a form submission handler to work with ajax
file uploads: when submission is requested while files are still being processed,
the form will be submitted when all files complete.

File uploads are POSTed to the configured url with these HTTP headers:

  Content-Disposition:  filename="original_file.ext"
  Content-Type
  Content-MD5

To display different instructions depending on whether or not the browser
supports the HTML5 methods required for this MD5 uploader, use something
like the following:

    <p class="md5upload-not-supported">[not supported text]</p>
    <p class="md5upload-supported" style="display:none">
      [supported instructions text] </p>

When md5DropUploader detects that the browser supports required methods, it will
 show all .md5upload-supported elements and hide all .md5upload-not-supported
elements.

If you need to add external validation on a drop-upload form, in
addition to the usual logic your validation function should store a
boolean value in the data for the form element with a key of 'valid', e.g.:

  $('form').data('valid', false);

If the form 'valid' value is set to false, the drop-uploader submit
handler will stop processing and not submit the form.



Adapted in part from https://github.com/texel/drag_drop_example/

*/

(function( $ ){

  function browser_upload_support() {
    // check for html5 file api
    if (typeof window.FileReader != 'function')
      return false;

    // check for blob slicing.
    // NB: deciding where all the conditionals and branches go and who gets
    // else clauses is actually a little subtle.
    // NOTE: Chrome considers window.Blob and window.File to be functions, but
    // Firefox considers them objects - either should be OK for our purposes
    var blob_slicing = false;
    // if we have a Blob and it can slice, then we have blob slicing
    if ((typeof window.Blob == 'function' || typeof window.Blob == 'object') &&
        (typeof window.Blob.prototype.slice == 'function')) {
          blob_slicing = true;
    }
    // if we have a File and it can slice, then we have blob slicing
    if ((typeof window.File == 'function' || typeof window.File == 'object') &&
        (typeof window.File.prototype.slice == 'function' ||
        // As of May 2011, the most recent versions of Google Chrome and Firefox 4
        // provide namespaced versions of the slice method (new spec).
         typeof window.File.prototype.webkitSlice == 'function' ||
         typeof window.File.prototype.mozSlice == 'function')) {
          blob_slicing = true;
    }
    // otherwise, the browser doesn't have what we need.
    if ( ! blob_slicing )
      return false;

    // looks like we have everything we need.
    return true;
  }

  var methods = {

    /**
     * Initialize the object:
     * configure settings, add special upload & submit button, and
     * bind methods as event handlers.
     * If HTML5 File API is not available, does nothing.
     */
    init : function(options) {

    return this.each(function(){
       if ( ! browser_upload_support() ) {
         return;
       }
       // show supported text, hide not-supported text
       $('.md5upload-supported').show();
       $('.md5upload-not-supported').hide();

       var $this = $(this);
       var data = {
         file_count: 0,
         files: new Array(),
         ingest_on_completion: false,
         allowed_types: [],
         csrf_token: null
       };
       $.extend(data, options);
       $this.addClass('md5uploader');

       // following recommended practice: store data in one object with name of plugin
       $this.data('md5DropUploader', data);

       $this.bind('dragenter.md5DropUploader', methods.dragEnter);
       $this.bind('dragover.md5DropUploader', methods.dragOver);
       $this.bind('drop.md5DropUploader', methods.drop);
       $this.bind('dragleave.md5DropUploader', methods.dragLeave);
       // custom event to be triggered after a file is uploaded
       $this.bind('afterUpload.md5DropUploader', methods.afterUpload);

       // bind parent form submission event to custom submit handler
       $this.parents('form').submit(methods.submitForm);
       // add place-holder element for form submission status/information
       $this.parents('form').append($('<span id="submit-info"/>'));

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
    },

    /**
     * Process files that are dropped.  Add any allowed types to the stored
     * list of files, then MD5 sum and upload each of them, reporting
     * status and progress to the user.
     */
    drop : function(event) {
      var $this = $(this);
      $this.removeClass('dragover');
      event.stopPropagation();
      event.preventDefault();

      // store current file count - marker for where to start processing in full list of files
      var start_processing = $this.data('md5DropUploader').file_count;
      var allowed_types =  $this.data('md5DropUploader').allowed_types;
      var not_allowed = new Array();
      // display files if they are allowed type, add to list of all files
      if (event.originalEvent.dataTransfer.files.length > 0) {
        $.each(event.originalEvent.dataTransfer.files, function ( i, file ) {
            // if allowed types have been specified, check that file is one of the specified types
            if (allowed_types.length == 0 ||
                $.inArray(file.type, allowed_types) != -1) {    // returns index or -1 if not found
                // rudimentary list display

                var p = $('<p><a class="remove">X</a> ' + file.name + ' ' +
                    '<span class="file-info">(' + filesize_format(file.size) +
		    ', ' + file.type + ')</span></p>');
                $this.append(p);
                // create status node and attach to file so it is easy to update
                file.status = $('<span class="status">-</span>');
                p.append(file.status);
                $this.data('md5DropUploader').files.push(file);
                $this.data('md5DropUploader').file_count++;
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
            msg += "  " + file.name + "\t" + file.type + "\n";
          });
          alert(msg);
        }

       // handle files added on the current drop
       // - calculate checksum and then upload
       $.each($this.data('md5DropUploader').files, function(i, file) {
            // only process files added on the current drop
            if (i >= start_processing) {
                // update status
                file.status.html('calculating checksum');
                console.log(file.name + ' calculating checksum')
                var start_time = new Date();
                var indicator = $('<p/>');
                file.progress = $('<div class="progress-bar"/>');
                file.progress.append(indicator);
                file.status.append(file.progress);

                // create a streaming md5 calculator for this file
                var md5 = new MD5();
                var next_step = function() {
                  // this is what we'll do after checksumming is complete
                  // TODO: ideally this should use a real js event framework
                  var end_time = new Date();
                  console.log(file.name +
                              ' checksum calculation took ' +
                              ((end_time - start_time) / 1000) +
                              ' seconds.');
                  file.status.html('uploading');
                  $this.md5DropUploader('uploadFile', file);
                };
                // kick off the checksum process in the background.
                var kickoff_checksum = function() {
                  calculate_checksum(file, indicator, 0, md5, next_step);
                };
                setTimeout(kickoff_checksum, 0);

            }
         });
      };
      return false;
    },  // end drop method

    /**
     * After each file finishes uploading, if form submission has been
     * requested after upload completes and all dropped files have been
     * uploaded, submit the form.
     */
    afterUpload: function(event) {
        var $this = $(this);
        if ($this.data('md5DropUploader').submit_on_completion &&
                $this.md5DropUploader('allFilesUploaded')) {
            $this.parents('form').submit();
        }
    },

    /**
     * Check if all files that have been dragged in have completed uploading.
     * Returns true when all files have completed uploading, false if any have not.
     */
    allFilesUploaded: function() {
        // loop through all dropped files to check if upload has completed
        var $this = $(this);
        for (var x = 0; x < $this.data('md5DropUploader').files.length; x++) {
            if (! $this.data('md5DropUploader').files[x].upload_id) {
                return false;
            }
        }
        return true;
    },

    /* Form submission logic: don't submit the form while any dropped files are
     * still being processed, and allow user to click the button now to submit
     * the form after any in-progress uploads complete.
     * Used as form submission event handler.
     */
    submitForm: function(event) {
        var $this = $(this);
        // Support external validation: if a submit handler sets
        // 'valid' to false on the form, bail out.  Assumes the external
        // validation handles any errors/warnings.
        if ($this.data('valid') == false) {
            return false;
        }
        // retrieve the md5 upload element relative to the form
        var uploader = $this.find('.md5uploader');
        // check if any dropped files have not yet been uploaded
        if (! uploader.md5DropUploader('allFilesUploaded')) {
            // if all dropped files have not yet completed,
            // set a flag to submit the form when uploads complete
            uploader.data('md5DropUploader').submit_on_completion = true;

            // display a message to the user
            $this.find('#submit-info').html('The form will submit when all uploads complete.')

            // don't propagate the submit event
            event.stopPropagation();
            event.preventDefault();
            return false;
        }

        // otherwise, all dropped files have completed upload - submit normally
        $this.find('#submit-info').html('Submitting...')
        return true;
    },

    /**
     * Upload a file to the configured url via XMLHttpRequest.
     * When the request returns status 200, adds hidden form inputs.
     * On any other status code, sets file.upload_id to -1 to indicate
     * upload completed but did not succeed.
     * Triggers custom 'afterUpload' event after the request completes.
     */
    uploadFile: function(file) {
        var $this = $(this);
        // use jQuery ajax method?
        var xhr   = new XMLHttpRequest();

        // display upload progress bar
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

        xhr.open('POST', $this.data('md5DropUploader').url, true);
        if ($this.data('md5DropUploader').csrf_token !== null) {
            xhr.setRequestHeader('X-CSRFToken', $this.data('md5DropUploader').csrf_token);
        }

        // set header so django will recognize as ajax, and can optionally
        // exempt from CSRF checking (if specified in the view)
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        // set required headers for processing the file
        xhr.setRequestHeader('Content-Disposition', 'filename="' + file.name + '"');
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
                file.status.parent().append('<input type="hidden" name="uploaded_files" value="' + file.upload_id + '"/>');
                file.status.parent().append('<input type="hidden" name="filenames" value="' + file.name + '"/>');

             } else {
                console.log('response status is ' + xhr.status)
                var err_msg = 'Upload error'
                if (xhr.status == 0) {      // request aborted; could happen if not authorized/login session times out
                   file.status.html(err_msg + ': Request Aborted');
                } else if (xhr.status >= 400 && xhr.getResponseHeader('Content-Type') == 'text/plain') {
                  // other upload errors should normally return a plain-text error message
                   file.status.html('Upload error: ' + xhr.responseText);
                } else {
                   // if not plain-text, something probably went wrong (500/exception)
                   file.status.html('Upload error');
               }
               file.upload_id = -1;
               // TODO: include upload errors in the form somehow so that
               // we can report them on the form submission page
             }

             // signal the uploader for after-upload logic
             $this.trigger('afterUpload.md5DropUploader');
          }
        };

        xhr.send(file);
    }  // end uploadFile method
  };


  $.fn.md5DropUploader = function(method) {
    if ( methods[method] ) {
      return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
    } else if ( typeof method === 'object' || ! method ) {
      return methods.init.apply( this, arguments );
    } else {
      $.error( 'Method ' +  method + ' does not exist on jQuery.md5DropUploader' );
    }
  };

  /* Incrementally calculate a file checksum without eliminating browser
   * responsiveness.
   *   :param: file = the file (an html5 file object)
   *   :param: indicator = a dom element to update with progress
   *   :param: start = the file offset to start checksumming at
   *   :param: md5 = a streaming md5 calculator object
   *   :param: next_step = a function to call after md5 calculation
   * This method grabs a slice from the file starting at `start` and asks
   * the browser to load that slice. When the slice is loaded, this function
   * will update `indicator` and push the chunk's data into `md5`. If
   * there's more file to process, it'll recurse to handle the next slice.
   * Once all slices have been processed, it'll attach the checksum to the
   * file object and call `next_step`.
   */
  function calculate_checksum(file, indicator, start, md5, next_step) {
    var size = 1024 * 1024; // 1MB chunks seem to work well, but might still want tweaking

    // Due to changes in the HTML5 Blob/File spec for slice, Mozilla
    // and Webkit now have name-spaced slice functions that implement
    // the new version of the spec.  Use those first, if available.
    if (typeof window.Blob.prototype.webkitSlice == 'function') {
        // Google Chrome -  http://trac.webkit.org/changeset/83873
        var slice = file.webkitSlice(start, start + size);
    } else if (typeof window.Blob.prototype.mozSlice == 'function') {
        // Mozilla Firefox -  https://developer.mozilla.org/en/DOM/Blob
        var slice = file.mozSlice(start, start + size);
    } else {
        // Using the old-spec slice function for now:
        //   http://www.w3.org/TR/2009/WD-FileAPI-20091117/#dfn-Blob
        // Updated spec for Blob.slice (as implemented in mozSlice and webkitSlice):
        //   http://www.w3.org/TR/2010/WD-FileAPI-20101026/#dfn-Blob
    var slice = file.slice(start, size);
    }

    // make a reader for handling the current slice.
    var reader = new FileReader();
    reader.onloadend = function (evt){
      // after loading the slice update the ui
      // TODO: ideally ui updates should use a real js event framework and
      // live outside this function
      file.status.html('calculating checksum');
      var percentage = Math.round((start * 100) / file.size);
      indicator.width(percentage);
      indicator.html(percentage + '%');
      file.status.append(file.progress);

      // then ship the data to the md5 calculator
      md5.process_bytes(evt.target.result);

      if (start + size < file.size) {
        // if there are more chunks then kick off the next chunk.
        var process_next_slice = function () {
          calculate_checksum(file, indicator, start+size,
                             md5, next_step);
        };
        setTimeout(process_next_slice, 0);
      } else {
        // if we're done with the file then record the md5sum
        md5.finish();
        file.md5 = md5.asString();
        console.log(file.name + ' checksum ' + file.md5);
        // and go where the original caller asked us to
        next_step();
      }
    };
    // kick off the read that we just configured
    reader.readAsBinaryString(slice);
  }

})( jQuery );



// FIXME: where should filesize_format function go?
/* convert integer filesize in bytes to a human-readable format */
function filesize_format(size) {
    if (size === 0) {
        return '0 bytes';
    } else if (size < 100) {
        return '' + size + ' bytes';
    } else if (size < (1000 * 1000)) {
        size = '' +  size/1000;
        if (size.indexOf('.') != -1) {
            vals = size.split('.');
            size = vals[0] + '.' + vals[1].substring(0, 1);
        }
        return size + 'kb';
    } else {
        size = '' + size/(1000 * 1000);
        if (size.indexOf('.') != -1) {
            vals = size.split('.');
            size = vals[0] + '.' + vals[1].substring(0, 1);
        }
        return size + 'mb';
    }
    // TODO: gb ?
}


/* make console.log not an error even if console is not available */
if (!window.console) console = {};
console.log = console.log || function(){};
console.warn = console.warn || function(){};
console.error = console.error || function(){};
console.info = console.info || function(){};
