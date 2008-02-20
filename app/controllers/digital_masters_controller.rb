class DigitalMastersController < ApplicationController 
  # GETs should be safe (see http://www.w3.org/2001/tag/doc/whenToUseGet.html)
  verify :method => :post, :only => [ :destroy, :create, :update ],
         :redirect_to => { :action => :list }
  
  auto_complete_for :description_data, :mss_number, :limit => 20
  
  def index
    render :action => 'search'
  end 
  
  def searchAction
    #render_text @params.inspect
  
    @contents = Content.search(@params)
    render :action => 'list'
  end

  def dump
    @contents = Content.find(:all)
    render :action => 'dump', :layout => false
  end

  def list
    @content_pages, @contents = paginate :contents, :per_page => 50, :order => 'id'
  end

  def show
    @content = Content.find(params[:id])
  end

  def new
    redirect_to :action => 'edit', :view => 'data_entry'
  end
 
  def edit
    if params[:view]
      session[:view] = params[:view]
    end
  
    unless params[:id]
      @content = Content.new
    else
      @content = Content.find(params[:id])
    end  
    
    @ar = Array.new
    for access in @content.AccessRights
      @ar << AccessRight.find(access.id)
    end
    
  end

  def next 
    redirect_to :action => 'edit', :id => Content.findNext(params[:id])
  end

  def previous 
    redirect_to :action => 'edit', :id => Content.findPrevious(params[:id])
  end

  def update
    unless params[:id]
      @content = Content.new(params[:content])
      @content.created_at = Time::now
    else 
      @content = Content.find(params[:id])
    end
      
    @content.resource_type_id = params[:content][:resource_type_id]
    @content.other_id = params[:content][:other_id]
    @content.modified_at = Time::now
    
    unless (params[:content][:collection_number] == "No Collection")
      @content.collection_number = params[:content][:collection_number]
    else
      @content.collection_number = nil
    end
    
    @content.title = params[:content][:title]
    @content.subtitle = params[:content][:subtitle]
    @content.resource_type_id = params[:content][:resource_type_id]
    @content.location_id = params[:content][:location_id]
    @content.abstract = params[:content][:abstract]
    @content.toc = params[:content][:toc]
    @content.content_notes = params[:content][:content_notes]

    if (!params[:content][:data_entered_by].nil?)
      @content.data_entered_by = params[:content][:data_entered_by]
      @content.data_entered_date = Time::now
    end

    if (!params[:content][:authority_work_by].nil?)
      @content.authority_work_by = params[:content][:authority_work_by]
      @content.authority_work_date = Time::now
    end

    if (!params[:content][:initial_qc_by].nil?)
      @content.initial_qc_by = params[:content][:initial_qc_by]
      @content.initial_qc_date = Time::now
    end

    if (!params[:content][:completed_by].nil?)
      @content.completed_by = params[:content][:completed_by]
      @content.completed_date = Time::now
    end

    @content.languages.clear
    unless (params[:language][:languages0] == "")
      @content.languages << Language.find(params[:language][:languages0])    
    end
    unless (params[:language][:languages1] == "")
      @content.languages << Language.find(params[:language][:languages1])    
    end
    
    if @content.save
      flash[:notice] = 'Record saved successfully. ' #<a href="/digital_masters/edit/' + @content.id.to_s + '">Return to record.</a>'
      redirect_to :action => 'edit', :id => @content.id
    else
      render :action => 'edit'
    end
  end

  def destroy
    Content.find(params[:id]).destroy
    redirect_to :action => 'list'
  end
  
  
  
  
#############################################################################
# Contents Names
#############################################################################
  def showContentNames
    @content = Content.find(params[:id])
    
    render :partial => 'content_name_table'
  end  
  
  def addContentName
  
    @nc = ContentsNames.new
    @nc.content_id = params[:content_id]
    
    #display pop_up edit window loaded with partial name_form next action saveContentName
    render :partial => "popup_edit", :locals => {:partial_name => "name_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveContentName', :id => @nc}}}    
    
  end 
  
  def editContentName
  
    @nc = ContentsNames.find(params[:id])
    @n = Name.find(@nc.name_id)
    @r = Role.find(@nc.role_id)
    
    #display pop_up edit window loaded with partial name_form next action saveContentName
    render :partial => "popup_edit", :locals => {:partial_name => "name_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveContentName', :id => @nc}}}    
    
  end 
 
  def saveContentName
    
    unless params[:id]
      nc = ContentsNames.new
    else
      nc = ContentsNames.find(params[:id])
    end
      
    #update with new values  
    nc.content_id = params[:nc][:content_id]
    nc.name_id = params[:nc][:name_id]
    nc.role_id = params[:nc][:role_id]
      
    nc.save
    
    @content = Content.find(nc.content_id)    
    render :partial => 'content_name_table'
  end  
  
  def destroyContentName
    ContentsNames.find(params[:id]).destroy   
    
    @content = Content.find(params[:content_id])          
    render :partial => 'content_name_table'
  end  
  
#############################################################################
# Contents Subjects
#############################################################################
  def showContentSubjects
    @content = Content.find(params[:id])
    
    render :partial => 'content_subjects_table'
  end  
  
  def addContentSubject
  
    @cs = ContentsSubjects.new
    @cs.content_id = params[:content_id]
    
    #display pop_up edit window loaded with partial subjects_form next action saveContentSubject
    render :partial => "popup_edit", :locals => {:partial_name => "subject_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveContentSubject', :id => @cs}}}    
    
  end 
  
  def editContentSubject
  
    @cs = ContentsSubjects.find(params[:id])
    
    #display pop_up edit window loaded with partial subjects_form next action saveContentName
    render :partial => "popup_edit", :locals => {:partial_name => "subject_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveContentSubject', :id => @cs}}}    
    
  end 
 
  def saveContentSubject
    
    unless params[:id]
      cs = ContentsSubjects.new
    else
      cs = ContentsSubjects.find(params[:id])
    end
      
    #update with new values  
    cs.content_id = params[:cs][:content_id]
    cs.subject_id = params[:cs][:subject_id]
      
    cs.save
    
    @content = Content.find(cs.content_id)    
    render :partial => 'content_subjects_table'
  end  

  def destroyContentSubject
    ContentsSubjects.find(params[:id]).destroy   
    
    @content = Content.find(params[:content_id])          
    render :partial => 'content_subjects_table'
  end 
#############################################################################
# Contents Genres
#############################################################################
  def showContentGenres
    @content = Content.find(params[:id])
    
    render :partial => 'content_genres_table'
  end  
  
  def addContentGenre
  
    @cg = ContentsGenres.new
    @cg.content_id = params[:content_id]
    
    #display pop_up edit window loaded with partial genres_form next action saveContentGenres
    render :partial => "popup_edit", :locals => {:partial_name => "genre_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveContentGenre', :id => @cg}}}    
    
  end 
  
  def editContentGenre
  
    @cg = ContentsGenres.find(params[:id])
    
    #display pop_up edit window loaded with partial genres_form next action saveContentGenre
    render :partial => "popup_edit", :locals => {:partial_name => "genre_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveContentGenre', :id => @cg}}}    
    
  end 
 
  def saveContentGenre
    
    unless params[:id]
      cg = ContentsGenres.new
    else
      cg = ContentsGenres.find(params[:id])
    end
      
    #update with new values  
    cg.content_id = params[:cg][:content_id]
    cg.genre_id = params[:cg][:genre_id]
      
    cg.save
    
    @content = Content.find(cg.content_id)    
    render :partial => 'content_genres_table'
  end

  def destroyContentGenre
    ContentsGenres.find(params[:id]).destroy   
    
    @content = Content.find(params[:content_id])          
    render :partial => 'content_genres_table'
  end
#############################################################################
# Contents AccessRights
#############################################################################
  def showContentAccessRight
    @content = Content.find(params[:id])
    
    render :partial => 'content_accessrights_table'
  end  
  
  def addContentAccessRight
  
    @ar = AccessRight.new
    @ar.content_id = params[:content_id]
        
    #display pop_up edit window loaded with partial accessrights_form next action saveContentAccessRights    
    render :partial => "popup_edit", :locals => {:partial_name => "content_accessrights_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveContentAccessRights', :id => @ar}}}    
  end 
  
  def destroyContentAccessRight    
    AccessRight.find(params[:id]).destroy   
    
    @content = Content.find(params[:content_id])  
    
    @ar = Array.new
    for access in @content.AccessRights
      @ar << AccessRight.find(access.id)
    end
     
    render :partial => 'content_accessrights_table'
  end
  
  def editContentAccessRight
    @ar = AccessRight.find(params[:id])
     
    #display pop_up edit window loaded with partial accessrights_form next action saveContentAccessRights
    render :partial => "popup_edit", :locals => {:partial_name => "content_accessrights_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveContentAccessRights', :id => @ar}}}       
  end 
 
  def saveContentAccessRights

    unless params[:id]
      ar = AccessRight.new
    else
      ar = AccessRight.find(params[:id])
    end
      
    #update with new values  
    ar.content_id = params[:ar][:content_id]
    ar.restriction_id = params[:ar][:restriction_id]
    ar.restriction_other = params[:ar][:restriction_other]
    ar.name_id = params[:ar][:name_id]
    ar.copyright_date = params[:ar][:copyright_date]
      
    ar.save
    
    @content = Content.find(params[:ar][:content_id])  
    
    @ar = Array.new
    for access in @content.AccessRights
      @ar << AccessRight.find(access.id)
    end
      
    render :partial => 'content_accessrights_table'
  end
  
#############################################################################
# Still Images
#############################################################################  
  def addSrcStillImage

      @srcStillImage = SrcStillImage.new
      @srcStillImage.content_id = params[:content_id]
      @content = Content.find(params[:content_id])
      
      render :partial => "popup_edit", :locals => {:partial_name => "still_img_subform", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveSrcStillImage', :id => @srcStillImage}}}    
  end
  
  def editSrcStillImage
    @srcStillImage = SrcStillImage.find(params[:id])
    render :partial => "popup_edit", :locals => {:partial_name => "still_img_subform", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveSrcStillImage', :id => @srcStillImage}}}    
  end
  
  def saveSrcStillImage
    unless params[:id]
      srcStillImage = SrcStillImage.new
      @content = Content.find(params[:srcStillImage][:content_id])
    else
      srcStillImage = SrcStillImage.find(params[:id])
      @content = Content.find(srcStillImage.content_id)
    end    
    
    srcStillImage.form_id = params[:srcStillImage][:form_id]
    srcStillImage.dimension_height = params[:srcStillImage][:dimension_height]
    srcStillImage.dimension_height_unit = params[:srcStillImage][:dimension_height_unit]
    srcStillImage.dimension_width = params[:srcStillImage][:dimension_width]
    srcStillImage.dimension_width_unit = params[:srcStillImage][:dimension_width_unit]    
    srcStillImage.dimension_note = params[:srcStillImage][:dimension_note]
    srcStillImage.disposition = params[:srcStillImage][:disposition]
    srcStillImage.generation = params[:srcStillImage][:generation]
    srcStillImage.source_note = params[:srcStillImage][:source_note]
    srcStillImage.related_item = params[:srcStillImage][:related_item]
    srcStillImage.item_location = params[:srcStillImage][:item_location]
    srcStillImage.content_id = params[:srcStillImage][:content_id]
    srcStillImage.housing_id = params[:srcStillImage][:housing_id]
    srcStillImage.conservation_history = params[:srcStillImage][:conservation_history]
    srcStillImage.source_date = params[:srcStillImage][:source_date]
    srcStillImage.publication_date = params[:srcStillImage][:publication_date]
    
    srcStillImage.save
    
    render :partial => 'src_still_image_reload'
  end
  
  def destroySrcStillImage
    SrcStillImage.find(params[:id]).destroy
    @content = Content.find(params[:content_id])
    render :partial => 'src_still_image_reload'
  end
#############################################################################
# Tech Images
#############################################################################  
  def addTechImage

      @techImage = TechImage.new
      @techImage.src_still_image_id = params[:src_still_image_id]
      
      render :partial => "popup_edit", :locals => {:partial_name => "tech_image_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveTechImage', :id => @TechImage, :src_still_image_id => @techImage.src_still_image_id}}}    
  end
  
  def editTechImage
    @tech_image = TechImage.find(params[:id])
    render :partial => "popup_edit", :locals => {:partial_name => "tech_image_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveTechImage', :id => @tech_image, :src_still_image_id => @tech_image.src_still_image_id}}}    
  end
  
  def saveTechImage
    unless params[:id]
      tech_image = TechImage.new
    else
      tech_image = TechImage.find(params[:id])
    end    
    
    tech_image.src_still_image_id = params[:tech_image][:src_still_image_id]
    tech_image.deriv_filename     = params[:tech_image][:deriv_filename]    
    tech_image.date_captured      = params[:tech_image][:date_captured]    
    tech_image.methodology        = params[:tech_image][:methodology]    
    tech_image.scale              = params[:tech_image][:scale]    
    tech_image.scanner_camera_id  = params[:tech_image][:scanner_camera_id]    
    tech_image.target_id          = params[:tech_image][:target_id]    
    tech_image.file_location      = params[:tech_image][:file_location]    
    tech_image.image_processing   = params[:tech_image][:image_processing]    
    tech_image.image_note         = params[:tech_image][:image_note]    
    
    tech_image.save
    
    @content = Content.find(SrcStillImage.find(tech_image.src_still_image_id).content_id)    
    
    render :partial => 'src_still_image_reload'
  end  

  def destroyTechImage
    TechImage.find(params[:id]).destroy
    @content = Content.find(params[:content_id])    
    
    render :partial => 'src_still_image_reload'
  end
#############################################################################
# Sounds
#############################################################################  
  def addSrcSound

      @src_sound = SrcSound.new
      @src_sound.content_id = params[:content_id]
      @content = Content.find(params[:content_id])
      
      render :partial => "popup_edit", :locals => {:partial_name => "src_sound_subform", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveSrcSound', :id => @src_sound}}}    
  end
  
  def editSrcSound
    @src_sound = SrcSound.find(params[:id])
    render :partial => "popup_edit", :locals => {:partial_name => "src_sound_subform", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveSrcSound', :id => @src_sound}}}    
  end
  
  def saveSrcSound
    unless params[:id]
      srcSound = SrcSound.new
      @content = Content.find(params[:src_sound][:content_id])
    else
      srcSound = SrcSound.find(params[:id])
      @content = Content.find(srcSound.content_id)
    end    
    
    srcSound.form_id = params[:src_sound][:form_id]
    srcSound.reel_size = params[:src_sound][:reel_size]
    srcSound.dimension_note = params[:src_sound][:dimension_note]
    srcSound.disposition = params[:src_sound][:disposition]
    srcSound.gauge = params[:src_sound][:gauge]
    srcSound.generation = params[:src_sound][:generation]
    srcSound.length = params[:src_sound][:length]
    srcSound.source_note = params[:src_sound][:source_note]
    srcSound.sound_field = params[:src_sound][:sound_field]
    srcSound.speed_id = params[:src_sound][:speed_id]
    srcSound.stock = params[:src_sound][:stock]
    srcSound.tape_thick = params[:src_sound][:tape_thick]
    srcSound.track_format = params[:src_sound][:track_format]
    srcSound.related_item = params[:src_sound][:related_item]
    srcSound.item_location = params[:src_sound][:item_location]
    srcSound.content_id = params[:src_sound][:content_id]
    srcSound.housing_id = params[:src_sound][:housing_id]
    srcSound.conservation_history = params[:src_sound][:conservation_history]
    srcSound.source_date = params[:src_sound][:source_date]
    srcSound.publication_date = params[:src_sound][:publication_date]
    srcSound.transfer_engineer_staff_id = params[:src_sound][:transfer_engineer_staff_id]
    
    srcSound.save
    
    render :partial => 'src_sound_reload'
  end
  
  def destroySrcSound
    SrcSound.find(params[:id]).destroy
    @content = Content.find(params[:content_id])
    
    render :partial => 'src_sound_reload'
  end
#############################################################################
# Tech Sounds
#############################################################################  
  def addTechSound

      @tech_sound = TechSound.new
      @tech_sound.src_sound_id = params[:src_sound_id]
      
      render :partial => "popup_edit", :locals => {:partial_name => "tech_sound_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveTechSound', :id => @TechImage, :src_sound_id => @tech_sound.src_sound_id}}}    
  end
  
  def editTechSound
    @tech_sound = TechSound.find(params[:id])
    render :partial => "popup_edit", :locals => {:partial_name => "tech_sound_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveTechSound', :id => @tech_sound, :src_sound_id => @tech_sound.src_sound_id}}}    
  end
  
  def saveTechSound
    unless params[:id]
      tech_sound = TechSound.new
    else
      tech_sound = TechSound.find(params[:id])
    end    
    
    tech_sound.src_sound_id       = params[:tech_sound][:src_sound_id]
    tech_sound.format_name        = params[:tech_sound][:format_name]    
    tech_sound.byte_order         = params[:tech_sound][:byte_order]    
    tech_sound.compression_scheme = params[:tech_sound][:compression_scheme]    
    tech_sound.file_size          = params[:tech_sound][:file_size]    
    tech_sound.codec_creator      = params[:tech_sound][:codec_creatoe]    
    tech_sound.codec_quality      = params[:tech_sound][:codec_quality]    
    tech_sound.methodology        = params[:tech_sound][:methodology]    
    tech_sound.bits_per_sample    = params[:tech_sound][:bits_per_sample]    
    tech_sound.sampling_frequency = params[:tech_sound][:sampling_frequency]    
    tech_sound.sound_note         = params[:tech_sound][:sound_note]
    tech_sound.duration           = params[:tech_sound][:duration]
    tech_sound.file_location      = params[:tech_sound][:file_location]
    tech_sound.sound_clip         = params[:tech_sound][:sound_clip]                
    tech_sound.digital_provenance_id = params[:tech_sound][:digital_provenance_id] 
    tech_sound.src_sound_id       = params[:tech_sound][:src_sound_id] 
    
    tech_sound.save
    
    @content = Content.find(SrcSound.find(tech_sound.src_sound_id).content_id)    
    
    render :partial => 'src_sound_reload'
  end  
  
  def destroyTechSound
    TechSound.find(params[:id]).destroy
    @content = Content.find(params[:content_id])    
    render :partial => 'src_sound_reload'    
  end
#############################################################################
#AJAX Responders
#############################################################################
  def getNow
    if (params[:completed_by] != '0')
      render_text(Time::now)
    else
      render_text('&nbsp;')
    end
  end

  def updateMainEntry
    #return main_entry when Collection Number is changed
    unless (params[:mss_number] == "")
      dd = DescriptionData.find_by_mss_number(params[:mss_number])    
      render_text(dd.main_entry)
    else
      render_text("")
    end
  end
  def updateTitleStatement
    #return TitleStatement when Collection Number is changed
    unless (params[:mss_number] == "")    
      dd = DescriptionData.find_by_mss_number(params[:mss_number])    
      render_text(dd.title_statement)
    else
      render_text("")
    end      
  end   
  def updateCollectionNumberID
    #return id field in a hidden field
    unless (params[:mss_number] == "")    
      dd = DescriptionData.find_by_mss_number(params[:mss_number])    
      id = dd.id.to_s
    else
      id = ""
    end      
    render_text('<input id="content_collection_number" maxlength="3" name="content[collection_number]" type="hidden" value="' + id + "'>")  
  end
end


