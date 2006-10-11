class Content < ActiveRecord::Base
  belongs_to :DescriptionData, :foreign_key => "collection_number"
  #has_and_belongs_to_many :languages
  has_many :languages, :class_name => 'ContentsLanguages'
  belongs_to :Location
  has_and_belongs_to_many :names
  belongs_to :ResourceType
  has_many :src_still_images
  belongs_to :StaffName, :foreign_key => "completed_by"
  has_and_belongs_to_many :subjects
  
  RECORD_ID_TYPES = [
    ["local", "local"], 
    ["Other - Record in Content Notes"]
  ].freeze  
  
  def self.find_by_image_note(noteText)    
    find(:all,
      :select     => 'c.id, c.record_id_type, c.other_id, c.date_created, c.date_modified, c.collection_number, c.title, c.subtitle, c.resource_type_id, c.location_id, c.abstract, c.toc, c.content_notes, c.completed_by, c.completed_date, c.complete',
      :joins      => 'AS c LEFT JOIN tech_images AS ti ON c.id = ti.content_id',
      :conditions => "\"ti\".\"image_note\" = '#{noteText}'")
  end

  def self.search(options)  
    conditions = "1=1 "
    joins = "AS c "
   if (options[:title] != '')
     conditions += "and c.title LIKE '%#{options[:title]}%'"
   end  
   if (options[:name] != nil and options[:name][:id] != '')
      joins += " LEFT JOIN contents_names as cn ON c.id = cn.content_id"
      conditions += "and cn.name_id = #{options[:name][:id]}"
      # role is only used in tandem with a name
      unless (options[:role][:id] == '')
        conditions += "and cn.role_id = #{options[:role][:id]}"  
      end 
   end
   if (options[:resource] != nil and options[:resource][:type] != '')
     conditions += "and c.resource_type_id = #{options[:resource][:type]}"
   end  
   if (options[:image_note] != '')
     joins += " LEFT JOIN tech_images AS ti ON c.id = ti.content_id "
     conditions += "and ti.image_note LIKE '%#{options[:image_note]}%'"
   end  
   if ( options[:image] != nil and options[:image][:format] != '')
     joins += " LEFT JOIN src_still_images AS ssi ON c.id = ssi.content_id "
     conditions += " and ssi.form_id = #{options[:image][:format]}"
   end
 
      
    find(:all,
#      :select     => 'c.id, c.record_id_type, c.other_id, c.date_created, c.date_modified, c.collection_number, c.title, c.subtitle, c.resource_type_id, c.location_id, c.abstract, c.toc, c.content_notes, c.completed_by, c.completed_date',
      :select     => '*',
      :joins      => joins,
      :conditions => conditions)
  end

end