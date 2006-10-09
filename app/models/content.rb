class Content < ActiveRecord::Base
  belongs_to :DescriptionData, :foreign_key => "collection_number"
  has_and_belongs_to_many :languages
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
      :conditions => '"ti"."image_note" = \'Dawson Grant\'')
  end

  
end