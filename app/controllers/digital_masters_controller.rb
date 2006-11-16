class DigitalMastersController < ApplicationController

  #verify :method => :post, :only => [ :destroy, :create, :update ],
  #       :redirect_to => { :action => :list }
  #verify :method => :post, :only => [ :saveContentGenre ],
  #       :redirect_to => { :action => :showContentGenres }  
  

  def index
    render :action => 'search'
  end 
  
  def searchAction
   @contents = Content.search(@params)
#    @content_pages = Paginator.new self, @contents.nitems, 25, @params['page']          
 #  render_text @params.inspect
    render :action => 'list'
  end

  # GETs should be safe (see http://www.w3.org/2001/tag/doc/whenToUseGet.html)
  verify :method => :post, :only => [ :destroy, :create, :update ],
         :redirect_to => { :action => :list }

  def list
    @content_pages, @contents = paginate :contents, :per_page => 25, :order => 'id'
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
      flash[:notice] = 'Record saved successfully. <a href="/digital_masters/edit/' + @content.id.to_s + '">Return to record.</a>'
      redirect_to :action => 'list'
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
    nc.role_term = params[:nc][:role_term]
      
    nc.save
    
    @content = Content.find(nc.content_id)    
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
    cs.fieldnames = params[:cs][:fieldnames]

      
    cs.save
    
    @content = Content.find(cs.content_id)    
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
    cg.fieldnames = params[:cg][:fieldnames]

      
    cg.save
    
    @content = Content.find(cg.content_id)    
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
    unless (params[:collection_number] == "")
      dd = DescriptionData.find(params[:collection_number])    
      render_text(dd.main_entry)
    else
      render_text("")
    end
  end
  def updateTitleStatement
    #return TitleStatement when Collection Number is changed
    unless (params[:collection_number] == "")    
      dd = DescriptionData.find(params[:collection_number])    
      render_text(dd.title_statement)
    else
      render_text("")
    end      
  end   
  
  def getSubjectAuthority
    #render_text (Subject.find(params[:subject_id]).Authority.authority)
    render_text (Subject.find(22).Authority.authority)
  end 
end
