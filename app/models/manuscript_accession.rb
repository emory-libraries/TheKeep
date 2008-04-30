class ManuscriptAccession < ActiveRecord::Base
  set_table_name '"Description Data"'
  set_primary_key 'ID'
  
  def self.fixDatabase
    #restore sequence
    last_ma = self.find(:first, :select => 'MAX("ID") as id' )
    new_ma_id = last_ma[:id].to_i + 1

    self.connection.execute("SELECT SETVAL('\"Description Data_ID_seq\"', #{new_ma_id})")
    
    #insert No Collection with ID=0
    self.connection.execute("INSERT INTO \"Description Data\" (\"ID\", \"Main Entry\", \"Title Statement\", \"MSS Number\", \"Description Y/N\", \"Type\", \"MSWord File Name\", \"RLIN ID Number\", \"XML\", \"Notes\") VALUES (0,'No Collection','No Collection',0,NULL,NULL,NULL,NULL,NULL,NULL)")
    
    #restore privileges
    self.connection.execute('GRANT ALL ON "Accession Records", "Accession Records_Record ID_seq", "Description Data", "Description Data Bak", "Description Data_ID_seq", "Purchase-Appraisal Table" TO digmast_user')
  end
end
